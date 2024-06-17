from flask import flash
from wtforms.validators import ValidationError
import re
import nh3
from urllib.error import HTTPError
from requests import Session, exceptions


def file_format():
    def _file_format(form, field):

        # Check if filesize is below 5MB
        if field.data:
            max_size = 5 * 1024 * 1024  # 5MB
            if field.data.content_length > max_size:
                raise ValidationError('File size must be less than 5MB.')

    return _file_format


def image_url():
    def _image_url(form, field):

        if not field.data or field.data == "":
            return

        allowed_filetypes = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/webp"]
        session = Session()

        try:
            request = session.get(field.data)
        except HTTPError as error:
            if error.code == 403:
                raise ValidationError("Access to the URL is forbidden")
            else:
                raise ValidationError("URL must be a valid image link")
        except exceptions.ConnectionError:
            raise ValidationError("Invalid URL. The server could not be reached.")
        except exceptions.MissingSchema:
            raise ValidationError("URL must be a valid image link")
        except Exception:
            raise ValidationError("Unforeseen error occurred while validating URL")

        else:
            if request.headers["content-type"] not in allowed_filetypes:
                raise ValidationError("URL must be a valid image link")

    return _image_url


def date_is_after(form):
    if ((form.start_year.data, form.start_month.data, form.start_day.data)
            > (form.end_year.data, form.end_month.data, form.end_day.data)):
        flash("DATE: End Date must be after Start Date")
        return False

    return True


def plain_text_length(max=600, required=False):
    def _plain_text_length(form, field):

        plain_text = nh3.clean(field.data, tags=set())

        if required and len(plain_text) == 0:
            raise ValidationError("This field is required")
        if max is not None:
            if len(plain_text) > max:
                raise ValidationError(f"Field must be less than {max} characters")

    return _plain_text_length
