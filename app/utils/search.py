from flask import url_for
from sqlalchemy import or_, func
import editdistance
from bs4 import BeautifulSoup

from app import db
from app import models


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
        excluded_event_columns = [
            "id",
            "url_title",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "second",
            "header",
            "hide_time",
            "campaign_id",
            "following_event_id"
        ]

        excluded_epoch_columns = [
            "id",
            "url_title",
            "start_year",
            "start_month",
            "start_day",
            "end_year",
            "end_month",
            "end_day",
            "has_events",
            "campaign_id"
        ]

        event_columns = [func.lower(column).label(column.name) for column in models.Event.__table__.columns
                         if column.name not in excluded_event_columns]

        epoch_columns = [func.lower(column).label(column.name) for column in models.Epoch.__table__.columns
                         if column.name not in excluded_epoch_columns]

        # Construct .like statements for each column using given search query
        event_query_filter = or_(*[column.like(f"%{query}%") for column in event_columns])
        epoch_query_filter = or_(*[column.like(f"%{query}%") for column in epoch_columns])

        # Filter the Event model objects based on the query filter
        event_results = (db.session.query(models.Event)
                         .join(models.Campaign.events)
                         .filter(models.Campaign.id == campaign.id, event_query_filter)
                         .all())

        # Filter the Event model objects based on the query filter
        epoch_results = (db.session.query(models.Epoch)
                         .join(models.Campaign.epochs)
                         .filter(models.Campaign.id == campaign.id, epoch_query_filter)
                         .all())

        all_results = event_results + epoch_results

        # Create event Result objects
        for item in all_results:

            result = Result()
            result.object = item

            if isinstance(item, models.Event):
                result.type = "Event"
                result.url = url_for("event.view_event",
                                     campaign_name=campaign.url_title,
                                     campaign_id=campaign.id,
                                     event_name=item.url_title,
                                     event_id=item.id)

                result.edit_url = url_for("event.edit_event",
                                          campaign_name=campaign.url_title,
                                          campaign_id=campaign.id,
                                          event_name=item.url_title,
                                          event_id=item.id)

                table_columns = event_columns

            elif isinstance(item, models.Epoch):
                result.type = "Epoch"
                result.url = url_for("epoch.view_epoch",
                                     campaign_name=campaign.url_title,
                                     campaign_id=campaign.id,
                                     epoch_title=item.url_title,
                                     epoch_id=item.id)

                result.edit_url = url_for("epoch.edit_epoch",
                                          campaign_name=campaign.url_title,
                                          campaign_id=campaign.id,
                                          epoch_title=item.url_title,
                                          epoch_id=item.id)

                table_columns = epoch_columns

            scores = []

            # Find the matching event attributes
            for column in table_columns:
                attr_value = getattr(item, column.name)
                if query in str(attr_value).lower():

                    matching_words = []
                    result.matching_attributes.append(column.name)
                    result.excerpt = self.create_excerpt(item)

                    # Convert html value entries to plain text
                    html_columns = ["description", "overview"]
                    if column.name in html_columns:
                        soup = BeautifulSoup(attr_value, "html.parser")
                        value = soup.get_text()
                    else:
                        value = attr_value

                    for word in value.split(" "):
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
    def create_excerpt(item):

        if isinstance(item, models.Event):
            excerpt_html = item.body
        elif isinstance(item, models.Epoch):
            excerpt_html = item.description or item.overview

        # Convert html to plaintext with BeautifulSoup
        if excerpt_html is not None:
            soup = BeautifulSoup(excerpt_html, "html.parser")
            plain_text = soup.get_text()

            # Ignore words within header tags
            for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                header_text = header.get_text()
                plain_text = plain_text.replace(header_text, "")

            excerpt = " ".join(plain_text.split()[:30])
            return f"{excerpt}..."
        else:
            return None
        