import smartpy as sp 
 
 
#Tournament organizer and participant both must send twice the prize value, this ensures that both the entities are committed to see the transaction to the end 
 
class Escrow(sp.Contract):  
    def __init__(self): 
        # self.init(param) 
        self.init(organizer = sp.none, participant = sp.none, prize =sp.nat(0)) 
 
    @sp.entry_point 
    def setOrganizer(self, params): 
        #ensure organizer is not set already 
        sp.verify(~self.data.organizer.is_some()) 
 
        #the organizer sets the prize and must send 2x the prize in tex 
        self.data.prize = params.prize 
 
        sp.verify_equal(sp.amount,sp.utils.nat_to_tez(2 * self.data.prize),message="condition not met") 
        self.data.organizer = sp.some(sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B")) 
    @sp.entry_point 
    def setParticipant(self): 
        #ensure that organizer exists 
        sp.verify(self.data.organizer.is_some()) 
 
        #ensure that participant has not been set already 
        sp.verify(~self.data.participant.is_some()) 
 
        sp.verify(sp.amount == sp.utils.nat_to_tez(self.data.prize / 10)) 
        self.data.participant = sp.some(sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B")) 
 
    @sp.entry_point 
    def confirmReceived(self): 
        sp.verify_equal(sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B") , self.data.participant.open_some()) 
        sp.send(self.data.participant.open_some(), sp.utils.nat_to_tez(self.data.prize)) 
        sp.send(self.data.organizer.open_some(), sp.balance) 
        self.resetContract() 
 
    @sp.entry_point 
    def refundParticipant(self): 
        sp.verify_equal(sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B") , self.data.organizer.open_some()) 
        sp.send(self.data.participant.open_some(), sp.utils.nat_to_tez(self.data.prize / 10)) 
        sp.send(self.data.organizer.open_some(), sp.balance)  
        self.resetContract() 
 
 
@sp.add_test(name = "Escrow Test") 
def testEscrow():  
    html="" 
    organizer="AA" 
    participant="BB" 
     
     
    scenario = sp.test_scenario() 
    c1 = Escrow() 
    scenario += c1 
 
    print(scenario, "file")
    # set organizer and prize 
    html += scenario.setOrganizer(prize=1).run(sender = sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B"), amount = sp.tez(2),valid=False).html() 
     
    #set participant 
    html += scenario.setParticipant("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B").run(amount = sp.utils.nat_to_tez(2)).html() 
 
    #participant receives prize 
    html += scenario.confirmReceived().run(sp.address("tz1i18rfRPzpyNidRnnASEBayg3BHB9MLH8B")).html() 
 
    #organizer 
    html += scenario.refundParticipant().run(sp.address(organizer)).html() 
 
    setOutput(html)