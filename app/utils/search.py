from flask import url_for
from sqlalchemy import or_, func
import editdistance
import re
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
        self.matching_strings = []
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
        return sorted(self.results, key=lambda result: result.relevance, reverse=True)

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

            searchable_columns = [column.name for column in table_columns]
            for attr, value in item.__dict__.items():
                if attr in searchable_columns:
                    if attr == "dynamic_fields":
                        for field in item.dynamic_fields:
                            
                            found = False
                            if query in field["title"].lower():
                                found = True
                                result.matching_strings.append(field["title"])

                            if field["field_type"] == "composite":
                                for group in field["value"]:
                                    # Check title of group
                                    if query in group["title"].lower():
                                        found = True
                                        result.matching_strings.append(group["title"])

                                    # Check all entries in group
                                    for entry in group["entries"]:
                                        if query in entry.lower():
                                            found = True
                                            result.matching_strings.append(entry)

                            else:
                                if field["field_type"] == "html":
                                    soup = BeautifulSoup(field["value"], "html.parser")
                                    text = soup.get_text()
                                    matches = self.find_phrase(query, text)
                                    for match in matches:
                                        found = True
                                        result.matching_strings.append(match)

                                elif field["field_type"] == "basic":
                                    matches = self.find_phrase(query, field["value"].lower())
                                    for match in matches:
                                        found = True
                                        result.matching_strings.append(match)

                            if found:
                                result.matching_attributes.append(field["title"])

                    # Handle static fields
                    else:
                        found = False
                        if query in attr.lower():
                            found = True
                            result.matching_strings.append(attr)
                        # Parse static HTML fields "eg. Epoch Overview, Description"
                        if attr in ["overview", "description"]:
                            soup = BeautifulSoup(value.lower(), "html.parser")
                            text = soup.get_text()
                            matches = self.find_phrase(query, text)
                        else:
                            matches = self.find_phrase(query, value.lower())

                        for match in matches:
                            found = True
                            result.matching_strings.append(match)
                        if found:
                            result.matching_attributes.append(attr)

            # Calculate relevance scores
            result.relevance = self.calculate_relevance(query, result.matching_strings)

            # Get excerpt text
            result.excerpt = self.create_excerpt(item)

            # Create matching attributes text for template
            result.matching_attributes_text = ", ".join(result.matching_attributes).title()

            self.results.append(result)


    @staticmethod
    def find_phrase(query, text):
        pattern = r"(?:^|\s|,|\.)([^\s,.]*?{0}[^\s,.]*?)(?:\s|,|\.|$)".format(re.escape(query))
        matches = re.findall(pattern, text, re.IGNORECASE)
        return matches


    @staticmethod
    def calculate_relevance(query, matching_strings):
        total_score = 0
        for string in matching_strings:
            # Calculate the edit distance
            distance = editdistance.eval(query, string)

            if distance > 0:
                score = 1 / distance
            else:
                score = 1  # If distance is 0 (exact match), set score to 1

            # Adjust score based on the length of the string
            score /= len(string)

            total_score += score

        # Multiply by the number of matching fields to give more weight to results with more matches
        total_score *= len(matching_strings)
        return total_score


    @staticmethod
    def create_excerpt(item):

        if isinstance(item, models.Event):
            fields = [field for field in item.dynamic_fields if field["field_type"] == "html"]
            fields = sorted(fields, key=lambda field: len(field["value"]), reverse=True)
            if len(fields) > 0:
                excerpt_html = fields[0]["value"]
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
        