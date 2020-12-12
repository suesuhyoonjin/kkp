# encoding: utf-8
from collections import OrderedDict

from django import VERSION, forms
from django.forms import ModelChoiceField
from django.forms.fields import CharField
from django.test import TestCase
from django.views.generic import View

from django_popup_view_field.fields import PopupViewField, PopupViewFieldMixin, PopupViewModelField


class FieldTest(TestCase):

    def test_subclass_field(self):
        assert issubclass(PopupViewField, (CharField, PopupViewFieldMixin)) is True
        assert issubclass(PopupViewModelField, (ModelChoiceField, PopupViewFieldMixin)) is True

    def test_form(self):

        class PopupView(View):
            pass

        class Form(forms.Form):
            popup_view_field = PopupViewField(view_class=PopupView)

        form = Form()
        assert form.is_valid() is False

        form = Form({'popup_view_field': 'test'})
        assert form.is_valid() is True
        assert form.cleaned_data.get("popup_view_field") == "test"

        form = Form()
        html = form.as_p()

        # Patch for django 1.10
        # In dj 1.10 required attribut is
        # added to input
        required = ""
        if VERSION >= (1, 10):
            required = "required"

        expected_html = '''
            <input
            id="id_popup_view_field"
            name="popup_view_field"
            type="text"
            class="form-control"
            {required}/>
        '''.format(required=required)

        self.assertInHTML(expected_html, html)
        assert html.find('''class="input-group-addon btn popup-view-btn-load"''') != -1
        assert html.find('''data-target="id_popup_view_field"''') != -1
        assert html.find('''data-popup-dialog-title="Popup Dialog: Select value"''') != -1
        assert html.find('''data-url = "/django_popup_view_field/PopupView/?"''') != -1

        class Form(forms.Form):
            popup_view_field = PopupViewField(
                view_class=PopupView,
                popup_dialog_title='Foo Bar Title Window',
                help_text='Test help text'
            )

        form = Form()
        html = form.as_p()
        assert html.find('''data-popup-dialog-title="Foo Bar Title Window"''') != -1
        self.assertInHTML('''<span class="helptext">Test help text</span>''', html)

    def test_readonly_field(self):

        class PopupView(View):
            pass

        required = ""
        if VERSION >= (1, 10):
            required = "required"

        class Form(forms.Form):
            popup_view_field = PopupViewField(
                view_class=PopupView,
                attrs={'readonly': True}
            )

        form = Form()
        html = form.as_p()

        expected_html = '''
            <input
            id="id_popup_view_field"
            name="popup_view_field"
            type="text"
            class="form-control"
            {required}
            readonly/>
        '''.format(required=required)

        self.assertInHTML(expected_html, html)

    def test_callback_data_type_error(self):

        class PopupView(View):
            pass

        with self.assertRaises(AttributeError):
            PopupViewField(view_class=PopupView, callback_data="wrong type")

    def test_callback_data(self):

        class PopupView(View):
            pass

        class Form(forms.Form):
            popup_view_field = PopupViewField(
                view_class=PopupView,
                callback_data=OrderedDict([
                    ('pk', 1),
                    ('name', "Some name"),
                    ('utf', "ąść"),
                    ('escape', '&?')
                ])
            )

        form = Form()
        html = form.as_p()
        assert (
            '"/django_popup_view_field/PopupView/'
            '?pk=1&amp;name=Some+name&amp;utf=%C4%85%C5%9B%C4%87&amp;escape=%26%3F"'
        ) in html
