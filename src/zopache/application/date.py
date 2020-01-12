# -*- coding: utf-8 -*-

import crom
import dateutil.parser

from cromlech.i18n import ILocale
from dolmen.forms.base import interfaces
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import DisplayFieldWidget, WidgetExtractor
from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces
from babel.dates import format_date, format_datetime
from babel.dates import parse_date


def register():
    registerSchemaField(DatetimeSchemaField, schema_interfaces.IDatetime)
    registerSchemaField(DateSchemaField, schema_interfaces.IDate)


class DatetimeSchemaField(SchemaField):
    """A datetime field.
    """


class DateSchemaField(SchemaField):
    """A date field.
    """


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(DateSchemaField, Interface, Interface)
class DateFieldWidget(SchemaFieldWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_date(value, format='short', locale=str(locale))


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DateSchemaField, Interface, Interface)
class DateWidgetExtractor(WidgetExtractor):

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if value:
                try:
                    locale = ILocale(self.request, default='en')
                    value = parse_date(value, locale=str(locale))
                    return value, error
                except (ValueError, IndexError) as err:
                    return None, 'Unknown date pattern'
            else:
                value = None
        return value, error


@crom.adapter
@crom.name('hidden')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DateSchemaField, Interface, Interface)
class HiddenDateWidgetExtractor(DateWidgetExtractor):
    pass


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeFieldWidget(DateFieldWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_datetime(value, format='short', locale=str(locale))


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeWidgetExtractor(DateWidgetExtractor):

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if value:
                try:
                    locale = ILocale(self.request, default='en')
                    value = dateutil.parser.parse(value)
                    return value, error
                except (ValueError, IndexError) as err:
                    return None, 'Unknown datetime pattern'
            else:
                value = None
        return value, error



@crom.adapter
@crom.name('hidden')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class HiddenDatetimeWidgetExtractor(DatetimeWidgetExtractor):
    pass



@crom.adapter
@crom.name('display')
@crom.target(interfaces.IWidget)
@crom.sources(DateSchemaField, Interface, Interface)
class DateFieldDisplayWidget(DisplayFieldWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_date(value, format='short', locale=str(locale))


@crom.adapter
@crom.name('display')
@crom.target(interfaces.IWidget)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeFieldDisplayWidget(DateFieldDisplayWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_datetime(value, format='short', locale=str(locale))
