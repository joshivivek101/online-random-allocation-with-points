from sheets import Sheet
import configs
import logics

class CandidateBase:
    def get_all(self):
        raise NotImplementedError()

class Candidate(CandidateBase):

    def __init__(self):
        self.sheet = Sheet()

    def get_all(self):
        cands = self.sheet.get_rows(configs.CANDIDATES_SHEET_ID, configs.CANDIDATES_SHEET_RANGE)
        return [{'id': cand[0], 'name': cand[1], 'email': cand[2]} for cand in cands]
    
    