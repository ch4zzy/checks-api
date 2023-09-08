from dynamic_preferences.preferences import Section
from dynamic_preferences.types import StringPreference
from dynamic_preferences.registries import global_preferences_registry

company = Section("company")


@global_preferences_registry.register
class CompanyName(StringPreference):
    section = company
    name = "company_name"
    default = "my_company"
    required = True
