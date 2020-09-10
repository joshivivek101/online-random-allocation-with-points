from candidates import Candidate
from match import Match
from allocations import Allocation
from optparse import OptionParser


def parse_command_line():
    parser = OptionParser()
    parser.add_option('--create-allocation', action='store_true', dest='allocate', default=False,
                      help='Allocate for new match')
    parser.add_option('--match-no', action='store', dest='match', help='match number')
     
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
            
            allocation_ser.create_allocation(match, allocations)

if __name__ == '__main__':
    exit(main())

