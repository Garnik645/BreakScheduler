from .template import BreakTemplateParser
from itertools import product


class DomainConstructor:
    def __init__(self, span_json, class_begin_time, class_end_time):
        templates = []
        for template_json in span_json:
            parser = BreakTemplateParser(template_json, class_begin_time, class_end_time)
            valid_interval_list = parser.construct_valid_interval_list()
            if valid_interval_list:
                templates.append(valid_interval_list)

        self.domain = list(product(*templates))
        for i, value in enumerate(self.domain):
            self.domain[i] = sorted(value)

    @staticmethod
    def is_domain_valid(value):
        for i in range(0, len(value) - 1):
            if value[i].end > value[i + 1].begin:
                return False
        return True

    @staticmethod
    def min_break_dist(domain):
        result = float('inf')
        for i in range(0, len(domain) - 1):
            result = min(result, domain[i + 1].begin - domain[i].end)
        return result

    def remove_invalid_values_from_domain(self):
        for i, value in enumerate(self.domain):
            if not self.is_domain_valid(value):
                del self.domain[i]

    def sort_domain_values(self):
        self.domain = sorted(self.domain, reverse=True, key=lambda domain: self.min_break_dist(domain))

    def get_domain_values(self, dist_lower_bound):
        result = []
        for value in self.domain:
            if self.min_break_dist(value) >= dist_lower_bound:
                result.append(value)
        return result
