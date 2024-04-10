from wtforms.validators import ValidationError
import re
import bleach

from urllib.error import HTTPError
from requests import Session



def date_format(format):

    if format == "event":
        message = "Not a valid date format, please use the format 'YYYY/MM/DD HH:MM:SS'"
        format = r"^-?\d{1,9}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$"
    elif format == "epoch":
        message = "Not a valid date format, please use the format 'YYYY/MM/DD'"
        format = r"^-?\d{1,9}/\d{2}/\d{2}$"

    def _date_format(form, field):

        if not re.match(format, field.data):
            raise ValidationError(message)

    return _date_format


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
        
        else:
            if request.headers["content-type"] not in allowed_filetypes:
                raise ValidationError("URL must be a valid image link")

    return _image_url


def date_is_after(form, field):
    start_date = form.start_date.data
    end_date = field.data

    # Convert to integers, catching exception if incorrect format submitted
    try:
        start_year, start_month, start_day = map(int, start_date.split("/"))
        end_year, end_month, end_day = map(int, end_date.split("/"))
    except ValueError:
        # The date_format validator will raise a Validation error already.
        return

    if (start_year, start_month, start_day) > (end_year, end_month, end_day):
        raise ValidationError("End Date must be after Start Date")


def plain_text_length(max=600):

    def _plain_text_length(form, field):
        plain_text = bleach.clean(field.data, tags=[], strip=True)
        if len(plain_text) > max:
            raise ValidationError(f"Field must be less than {max} characters")
        
    return _plain_text_length
