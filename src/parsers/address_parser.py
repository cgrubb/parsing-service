'''
Created on Mar 9, 2013
adapted from http://pyparsing.wikispaces.com/file/view/streetAddressParser.py/135329743/streetAddressParser.py
@author: cgrubb
'''
from pyparsing import *

# define number as a set of words
units = oneOf("Zero One Two Three Four Five Six Seven Eight Nine Ten"
          "Eleven Twelve Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen",
          caseless=True)
tens = oneOf("Ten Twenty Thirty Forty Fourty Fifty Sixty Seventy Eighty Ninety",caseless=True)
hundred = CaselessLiteral("Hundred")
thousand = CaselessLiteral("Thousand")
OPT_DASH = Optional("-")
numberword = ((( units + OPT_DASH + Optional(thousand) + OPT_DASH + 
                  Optional(units + OPT_DASH + hundred) + OPT_DASH + 
                  Optional(tens)) ^ tens ) 
               + OPT_DASH + Optional(units) )

# number can be any of the forms 123, 21B, 222-A or 23 1/2
housenumber = originalTextFor( numberword | Combine(Word(nums) + 
                    Optional(OPT_DASH + oneOf(list(alphas))+FollowedBy(White()))) + 
                    Optional(OPT_DASH + "1/2")
                    )
numberSuffix = oneOf("st th nd rd").setName("numberSuffix")
streetnumber = originalTextFor( Word(nums) + 
                 Optional(OPT_DASH + "1/2") +
                 Optional(numberSuffix) )

#nsew = (oneOf("N S E W North South East West NW NE SW SE") + Optional(".").suppress()).setName("direction")
#direction = originalTextFor(nsew)
direction_ = Combine(MatchFirst(map(Keyword, "N S E W North South East West NW NE SW SE".split())) + Optional(".").suppress())

# just a basic word of alpha characters, Maple, Main, etc.
name = ~numberSuffix + Word(alphas)

# types of streets - extend as desired
type_ = Combine( MatchFirst(map(Keyword,"Street St Boulevard Blvd Lane Ln Road Rd Avenue Ave "
                        "Circle Cir Cove Cv Drive Dr Parkway Pkwy Court Ct Square Sq"
                        "Loop Lp".split())) + Optional(".").suppress())

# street name
streetName = (Combine( streetnumber + 
                        Optional("1/2") + 
                        Optional(numberSuffix), joinString=" ", adjacent=False )
                ^ Combine(~numberSuffix + direction_)
                ^ Combine(OneOrMore(~type_ + Combine(Word(alphas) + Optional(".")) + ~direction_), joinString=" ", adjacent=False) 
                ^ Combine(~type_ + direction_)
                ^ Combine("Avenue" + Word(alphas), joinString=" ", adjacent=False)).setName("streetName")

# PO Box handling
acronym = lambda s : Regex(r"\.?\s*".join(s)+r"\.?")
poBoxRef = ((acronym("PO") | acronym("APO") | acronym("AFP")) + 
             Optional(CaselessLiteral("BOX"))) + Word(alphanums)("boxnumber")

# basic street address

streetReference = Optional(direction_).setResultsName("prefix_direction") + streetName.setResultsName("name") + Optional(type_).setResultsName("type") + Optional(direction_).setResultsName("suffix_direction")
direct = housenumber.setResultsName("number") + streetReference
intersection = ( streetReference.setResultsName("crossStreet") + 
                 ( oneOf('@ &') | Keyword("and",caseless=True)) +
                 streetReference.setResultsName("street") )
streetAddress = ( poBoxRef("street")
                  ^ direct.setResultsName("street")
                  ^ streetReference.setResultsName("street")
                  ^ intersection )

# how to add Apt, Suite, etc.
suiteRef = (
            oneOf("Suite Ste Apt Apartment Room Rm #", caseless=True) + 
            Optional(".") + 
            Word(alphanums+'-')("suitenumber"))
streetAddress = streetAddress + Optional(Suppress(',') + suiteRef("suite"))
