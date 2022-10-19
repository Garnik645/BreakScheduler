from cls.template import BreakTemplateParser
from itertools import product


class DomainConstructor:
    def __init__(self, span_json, class_begin_time, class_end_time):
        templates = []
        for template_json in span_json:
            parser = BreakTemplateParser(template_json, class_begin_time, class_end_time)
            templates.append(parser.construct_valid_interval_list())
        self.domains = list(product(*templates))
        for i, domain in enumerate(self.domains):
            self.domains[i] = sorted(domain)

    @staticmethod
    def is_domain_valid(domain):
        for i in range(0, len(domain) - 1):
            if domain[i].end > domain[i + 1].begin:
                return False
        return True

    @staticmethod
    def min_break_dist(domain):
        result = float('inf')
        for i in range(0, len(domain) - 1):
            result = min(result, domain[i + 1].begin - domain[i].end)
        return result

    def remove_invalid_domains(self):
        for i, domain in enumerate(self.domains):
            if not self.is_domain_valid(domain):
                del self.domains[i]

    def sort_domains(self):
        self.domains = sorted(self.domains, reverse=True, key=lambda domain: self.min_break_dist(domain))

    def get_domains(self, dist_lower_bound):
        result = []
        for domain in self.domains:
            if self.min_break_dist(domain) >= dist_lower_bound:
                result.append(domain)
        return result
