from candidates import Candidate
from match import Match
from allocations import Allocation
from optparse import OptionParser
from match_results import MatchResults
from logics import generate_candidate_result
from candidate_results import CandidateResult
from email_util import send_mail, generate_html_from_dics


def parse_command_line():
    parser = OptionParser()
    parser.add_option('--create-allocation', action='store_true', dest='allocate', default=False,
                      help='Allocate for new match')
    parser.add_option('--match-no', action='store',
                      dest='match', help='match number')

    parser.add_option('--generate-results', action='store_true', dest='results', default=False,
                      help='Generate result for match')

    (options, args) = parser.parse_args()
    return parser, options


def main():
    parser, options = parse_command_line()

    if options.allocate:
        if not options.match:
            raise Exception('Match number is required to create allocation')

        match_no = options.match
        cand = Candidate()
        candidates = cand.get_all()
        if candidates:
            allocation_ser = Allocation()
            allocations = allocation_ser.generate_allocation(candidates)
            match_ser = Match()
            match = match_ser.get(match_no)
            if not match:
                raise Exception('Match number not valid')

            aloc_values = allocation_ser.create_allocation(match, allocations)
            html_to_send = generate_html_from_dics(aloc_values)
            candidate_emails = [c['email'] for c in candidates]
            send_mail(candidate_emails, 'SS Dabba Party Allocation - Trip: '+match_no,'A refers to the team which will bat first and B is who is batting 2nd',html_to_send)

    elif options.results:
        if not options.match:
            raise Exception('Match number is required to create results')

        match_no = options.match
        result_service = MatchResults()
        results = result_service.get(match_no)

        aloc_service = Allocation()
        allocations = aloc_service.get_allocation(match_no)

        final_results = generate_candidate_result(allocations, results)

        match_service = Match()
        match_obj = match_service.get(match_no)

        cand_result_service = CandidateResult()
        result_values = cand_result_service.add_results(match_obj, final_results)
        html_to_send = generate_html_from_dics(result_values)
        candidate_emails = [res['name'] for res in final_results['results']]
        send_mail(candidate_emails, 'SS Dabba Party Result - Trip: '+match_no,'Result as following',html_to_send)

if __name__ == '__main__':
    exit(main())
