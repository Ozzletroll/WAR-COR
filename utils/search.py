from sqlalchemy import select, or_

from app import db
import models



class Result:
    """ Result object generated by SearchEngine """

    def __init__(self):
        self.relevenance = 0
        self.object = None
        self.excerpt = ""



class SearchEngine:

    """ Search engine class for searching within a campaign from the Advanced Search page. 

            Parameters:
            --------------------------------------
                results : list
                    List of Results objects.
            --------------------------------------

            Methods:

                return_results(self):
                    Returns a list of results objects
            
                search_campaign(self, campaign(obj), query(str)):
                    Searches the database for entries that match
                    the given search query, and creates Result
                    objects for each match. Appends them to
                    self.results.    
    """

    def __init__(self):
        self.results = []

  
    def return_results(self):

        for result in self.results:
            pass


        return self.results

    
    def search_campaign(self, campaign, query):

        # Get the columns of the Event model, excluding irrelevant ones
        excluded_columns = ["Year", "Month", "Day", "Hour", "Minute", "Second", "Header", "Hide Time"]
        columns = [column for column in models.Event.__table__.columns if column.name not in excluded_columns]

        # Construct .like statements for each column using given search query
        query_filter = or_(*[column.like(f"%{query}%") for column in columns])

        # Filter the Event model objects based on the query filter
        event_results = (db.session.query(models.Event)
                         .join(models.Campaign.events)
                         .filter(models.Campaign.id == campaign.id, query_filter).all()) 

        print(event_results)