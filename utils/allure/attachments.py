import allure
from decimal import Decimal
import json
from pandas import DataFrame


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def attach_text(text: str, name: str = "text report") -> None:
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


# def attach_element_screenshot(element, name: str = "element screenshot") -> None:
#     allure.attach(element.screenshot_as_png, name=name, attachment_type=allure.attachment_type.PNG)

def attach_screenshot(page, name: str = "page screenshot") -> None:
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


def attach_image(image: bytes, name: str = "image") -> None:
    allure.attach(image, name=name, attachment_type=allure.attachment_type.PNG)


def attach_element_attributes(element_details: dict) -> None:
    for attr_name, attr_value in element_details.items():
        allure.attach(attr_value, name=attr_name, attachment_type=allure.attachment_type.TEXT)


def attach_html(df: DataFrame, name: str = "pandas data"):
    html_data = df.to_html(
        index=False,
        classes='table table-striped table-bordered',
        border=1
    )
    allure.attach(html_data, name=name, attachment_type=allure.attachment_type.HTML)


def attach_json(product: dict, name: str = "product"):
    allure.attach(json.dumps(product, indent="\t", cls=DecimalEncoder), name=name,
                  attachment_type=allure.attachment_type.JSON)
