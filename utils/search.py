from flask import url_for
from sqlalchemy import or_
import editdistance
from bs4 import BeautifulSoup

from app import db
import models



class Result:
    """ Result object generated by SearchEngine """

    def __init__(self):
        self.relevance = 0
        self.object = None
        self.type = ""
        self.excerpt = ""
        self.matching_attributes = []
        self.matching_attributes_text = ""
        self.url = ""
        self.edit_url = ""



class SearchEngine:

    """ Search engine class for searching within a campaign from the Advanced Search page. 

            Parameters:
            --------------------------------------
                results : list
                    List of Results objects.
            --------------------------------------

            Methods:

                return_results(self):
                    Returns a list of results objects, sorted by
                    relevance value.
            
                search_campaign(self, campaign(obj), query(str)):
                    Searches the database for entries that match
                    the given search query, and creates Result
                    objects for each match. Appends them to
                    self.results.    
    """

    def __init__(self):
        self.results = []

  
    def return_results(self):
        return sorted(self.results, key=lambda result: result.relevance)

    
    def search_campaign(self, campaign, query):

        self.results = []
        query = query.lower()

        # Get the columns of the Event model, excluding irrelevant ones
        excluded_columns = ["id", 
                            "year", 
                            "month", 
                            "day", 
                            "hour", 
                            "minute", 
                            "second", 
                            "header", 
                            "hide_time",
                            "campaign_id",
                            "following_event_id"]
        
        columns = [column for column in models.Event.__table__.columns if column.name not in excluded_columns]

        # Construct .like statements for each column using given search query
        query_filter = or_(*[column.like(f"%{query}%") for column in columns])

        # Filter the Event model objects based on the query filter
        event_results = (db.session.query(models.Event)
                         .join(models.Campaign.events)
                         .filter(models.Campaign.id == campaign.id, query_filter)
                         .all()) 

        # Create Result objects
        for event in event_results:

            result = Result()
            result.object = event
            result.type = "Event"
            result.url = url_for("event.view_event",
                                 campaign_name=campaign.title,
                                 campaign_id=campaign.id,
                                 event_name=event.title,
                                 event_id=event.id)
            
            result.edit_url = url_for("event.edit_event",
                                      campaign_name=campaign.title,
                                      campaign_id=campaign.id,
                                      event_name=event.title,
                                      event_id=event.id)

            scores = []
            
            # Find the matching event attributes
            for column in columns:
                attr_value = getattr(event, column.name)
                if query in str(attr_value).lower():

                    matching_words = []
                    result.matching_attributes.append(column.name)
                    result.excerpt = self.create_excerpt(event)

                    for word in attr_value.split(" "):
                        if query in word.lower():
                            matching_words.append(word)

                        relevance = editdistance.eval(query, word)
                        scores.append(relevance)

            # Calculate final relevance score
            result.relevance = (sum(scores) / len(scores)) / len(scores)

            # Create matching attributes text for template
            result.matching_attributes_text = ", ".join(result.matching_attributes).title()

            self.results.append(result)


    @staticmethod
    def create_excerpt(event):

        excerpt_html = event.body

        # Convert html to plaintext with BeautifulSoup
        soup = BeautifulSoup(excerpt_html, "html.parser")
        plain_text = soup.get_text()

        # Ignore words within header tags
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            header_text = header.get_text()
            plain_text = plain_text.replace(header_text, "")
        
        excerpt = " ".join(plain_text.split()[:30])
        return f"{excerpt}..."
    