from dao.team_dao import TeamDAO

class TeamBuilder():

    def __init__(self):
        pass

    def createDefaultTeams(self):

        # self.provideDefaultTeam("fnatic", "https://www.hltv.org/team/4991/fnatic#tab-matchesBox", 1, 4991)
        # self.provideDefaultTeam("Natus Vincere", "https://www.hltv.org/team/4608/natus-vincere#tab-matchesBox", 2, 4608)
        # self.provideDefaultTeam("Astralis", "https://www.hltv.org/team/6665/astralis#tab-matchesBox", 3, 6665)
        # self.provideDefaultTeam("NiP", "https://www.hltv.org/team/4411/nip#tab-matchesBox", 13, 4411)
        # self.provideDefaultTeam("mousesports", "https://www.hltv.org/team/4494/mousesports#tab-matchesBox", 4, 4494)
        # self.provideDefaultTeam("Liquid", "https://www.hltv.org/team/5973/liquid#tab-matchesBox", 5, 5973)
        # self.provideDefaultTeam("G2", "https://www.hltv.org/team/5995/g2#tab-matchesBox", 6, 5995)
        # self.provideDefaultTeam("Evil Geniuses", "https://www.hltv.org/team/10399/evil-geniuses#tab-matchesBox", 7, 10399)
        # self.provideDefaultTeam("FaZe", "https://www.hltv.org/team/6667/faze#tab-matchesBox", 8, 6667)
        # self.provideDefaultTeam("Vitality", "https://www.hltv.org/team/9565/vitality#tab-matchesBox", 9, 9565)
        # self.provideDefaultTeam("100 Thieves", "https://www.hltv.org/team/8474/100-thieves#tab-matchesBox", 10, 8474)
        # self.provideDefaultTeam("FURIA", "https://www.hltv.org/team/8297/furia#tab-matchesBox", 11, 8297)
        # self.provideDefaultTeam("MAD Lions", "https://www.hltv.org/team/8362/mad-lions#tab-matchesBox", 12, 8362)
        # self.provideDefaultTeam("OG", "https://www.hltv.org/team/10503/og#tab-matchesBox", 14, 10503)
        # self.provideDefaultTeam("MIBR", "https://www.hltv.org/team/9215/mibr#tab-matchesBox", 15, 9215)
        # self.provideDefaultTeam("BIG", "https://www.hltv.org/team/7532/big#tab-matchesBox", 16, 7532)
        # self.provideDefaultTeam("forZe", "https://www.hltv.org/team/8135/forze#tab-matchesBox", 17, 8135)
        # self.provideDefaultTeam("GODSENT", "https://www.hltv.org/team/6902/godsent#tab-matchesBox", 18, 6902)
        # self.provideDefaultTeam("Spirit", "https://www.hltv.org/team/7020/spirit#tab-matchesBox", 19, 7020)
        # self.provideDefaultTeam("Virtus.pro", "https://www.hltv.org/team/5378/virtuspro#tab-matchesBox", 20, 5378)
        # self.provideDefaultTeam("North", "https://www.hltv.org/team/7533/north#tab-matchesBox", 21, 7533)
        # self.provideDefaultTeam("HAVU", "https://www.hltv.org/team/7865/havu#tab-matchesBox", 22, 7865)
        # self.provideDefaultTeam("Gen.G", "https://www.hltv.org/team/10514/geng#tab-matchesBox", 23, 10514)
        # self.provideDefaultTeam("Cloud9", "https://www.hltv.org/team/5752/cloud9#tab-matchesBox", 24, 5752)
        # self.provideDefaultTeam("ENCE", "https://www.hltv.org/team/4869/ence#tab-matchesBox", 25, 4869)
        # self.provideDefaultTeam("Complexity", "https://www.hltv.org/team/5005/complexity#tab-matchesBox", 26, 5005)
        # self.provideDefaultTeam("Gambit Youngsters", "https://www.hltv.org/team/9976/gambit-youngsters#tab-matchesBox", 50, 9976)
        # self.provideDefaultTeam("Nemiga","https://www.hltv.org/team/7969/nemiga#tab-matchesBox", 49, 7969)
        # self.provideDefaultTeam("AGO", "https://www.hltv.org/team/8068/ago#tab-matchesBox", 53, 8068)
        # self.provideDefaultTeam("c0ntact", "https://www.hltv.org/team/10606/c0ntact#tab-matchesBox", 37, 10606)
        # self.provideDefaultTeam("Espada", "https://www.hltv.org/team/8669/espada#tab-matchesBox", 52, 8669)
        # self.provideDefaultTeam("Hard Legion", "https://www.hltv.org/team/10421/hard-legion#tab-matchesBox", 48, 10421)
        # self.provideDefaultTeam("pro100", "https://www.hltv.org/team/7898/pro100#tab-matchesBox", 62, 7898)
        # self.provideDefaultTeam("Syman", "https://www.hltv.org/team/8772/syman#tab-matchesBox", 66, 8772)
        # self.provideDefaultTeam("Sprout", "https://www.hltv.org/team/8637/sprout#tab-matchesBox", 33, 8637)
        # self.provideDefaultTeam("Envy", "https://www.hltv.org/team/5991/envy#tab-matchesBox", 39, 5991)
        # self.provideDefaultTeam("Copenhagen Flames", "https://www.hltv.org/team/7461/copenhagen-flames#tab-matchesBox", 41, 7461)
        # self.provideDefaultTeam("TYLOO", "https://www.hltv.org/team/4863/tyloo#tab-matchesBox", 42, 4863)
        # self.provideDefaultTeam("SKADE", "https://www.hltv.org/team/10386/skade#tab-matchesBox", 38, 10386)
        # self.provideDefaultTeam("Nordavind", "https://www.hltv.org/team/8769/nordavind#tab-matchesBox", 45, 8769)
        # self.provideDefaultTeam("Heretics", "https://www.hltv.org/team/8346/heretics#tab-matchesBox", 29, 8346)
        # self.provideDefaultTeam("Dignitas", "https://www.hltv.org/team/5422/dignitas#tab-matchesBox", 40, 5422)
        # self.provideDefaultTeam("SMASH", "https://www.hltv.org/team/10315/smash#tab-matchesBox", 57, 10315)
        # self.provideDefaultTeam("Heroic", "https://www.hltv.org/team/7175/heroic#tab-matchesBox", 30, 7175)
        # self.provideDefaultTeam("Apeks", "https://www.hltv.org/team/9806/apeks#tab-matchesBox", 51, 9806)
        # self.provideDefaultTeam("Movistar Riders", "https://www.hltv.org/team/7718/movistar-riders#tab-matchesBox", 32, 7718)
        # self.provideDefaultTeam("Winstrike", "https://www.hltv.org/team/9183/winstrike#tab-matchesBox", 24, 9183)
        # self.provideDefaultTeam("FATE", "https://www.hltv.org/team/9863/fate#tab-matchesBox", 57, 9863)
        # self.provideDefaultTeam("Endpoint", "https://www.hltv.org/team/7234/endpoint#tab-matchesBox", 33, 7234)
        # self.provideDefaultTeam("sAw", "https://www.hltv.org/team/10567/saw#tab-matchesBox", 77, 10567)
        # self.provideDefaultTeam("PACT", "https://www.hltv.org/team/8248/pact#tab-matchesBox", 55, 8248)
        # self.provideDefaultTeam("Salamander", "https://www.hltv.org/team/9939/salamander#tab-matchesBox", 49, 9939)

        self.provideDefaultTeam("ALTERNATE aTTaX", "https://www.hltv.org/team/4501/alternate-attax#tab-matchesBox", 48, 4501)
        self.provideDefaultTeam("Secret", "https://www.hltv.org/team/10488/secret#tab-matchesBox", 46, 10488)
        self.provideDefaultTeam("Mythic", "https://www.hltv.org/team/5479/mythic#tab-matchesBox", 63, 5479)
        self.provideDefaultTeam("Chaos", "https://www.hltv.org/team/9085/chaos#tab-matchesBox", 41, 9085)
        self.provideDefaultTeam("KOVA", "https://www.hltv.org/team/9648/kova#tab-matchesBox", 75, 9648)
        self.provideDefaultTeam("AVEZ", "https://www.hltv.org/team/9797/avez#tab-matchesBox", 64, 9797)
        self.provideDefaultTeam("Excellency", "https://www.hltv.org/team/10727/excellency#tab-matchesBox", 47, 10727)
        self.provideDefaultTeam("BOOM", "https://www.hltv.org/team/7733/boom#tab-matchesBox", 56, 7733)


    def provideDefaultTeam(self, name, homepage, rank, hltv_id):
        team = TeamDAO().getTeamByLikeName(name)
        if team == None:
            TeamDAO().create_team(name, homepage, rank, hltv_id)
        else:
            TeamDAO().updateTeam(team, name, homepage, rank, hltv_id)
