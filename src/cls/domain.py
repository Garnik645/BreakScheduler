from template import BreakTemplateParser
from itertools import product


class DomainConstructor:
    def __init__(self, span_json, class_begin_time, class_end_time):
        templates = []
        for template_json in span_json:
            parser = BreakTemplateParser(template_json, class_begin_time, class_end_time)
            templates.append(parser.construct_valid_interval_list())
        self.domains = product(*templates)
        
    def remove_invalid_domains(self):
        pass
    
    def get_domain(self, dist_lower_bound_sec):
        pass