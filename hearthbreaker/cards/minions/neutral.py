from hearthbreaker.tags.action import Heal, Summon, Draw, \
    Kill, Damage, ResurrectFriendly, Steal, Duplicate, Give, SwapWithHand, AddCard, Transform, ApplySecret, \
    Silence, Bounce, GiveManaCrystal, Equip, GiveAura, Replace, SetHealth, Freeze, GiveEffect, ChangeTarget, Discard
from hearthbreaker.tags.aura import ManaAura
from hearthbreaker.tags.base import Effect, Deathrattle, CardQuery, CARD_SOURCE, Battlecry, Enrage, Aura, \
    BuffUntil, Buff
from hearthbreaker.tags.condition import Adjacent, IsType, MinionHasDeathrattle, IsMinion, IsSecret, \
    MinionIsTarget, IsSpell, IsDamaged, InGraveyard, ManaCost, OpponentMinionCountIsGreaterThan, AttackGreaterThan, \
    IsWeapon, HasStatus, AttackLessThanOrEqualTo, CardRarity, OneIn, NotCurrentTarget
from hearthbreaker.tags.event import TurnEnded, CardPlayed, MinionSummoned, TurnStarted, DidDamage, AfterAdded, \
    SpellCast, CharacterHealed, CharacterDamaged, MinionDied, CardUsed, MinionPlaced, Damaged, Attack, CharacterAttack
from hearthbreaker.tags.selector import MinionSelector, BothPlayer, BattlecrySelector, SelfSelector, \
    PlayerSelector, MinionCardSelector, TargetSelector, EnemyPlayer, CharacterSelector, SpellSelector, WeaponSelector, \
    HeroSelector, OtherPlayer, UserPicker, RandomPicker, CurrentPlayer
from hearthbreaker.cards.battlecries import gain_one_health_for_each_card_in_hand, deathwing
from hearthbreaker.game_objects import Minion, MinionCard, Card
from hearthbreaker.constants import CARD_RARITY, CHARACTER_CLASS, MINION_TYPE
from hearthbreaker.tags.status import ChangeAttack, ChangeHealth, ManaChange, Charge, Taunt, Windfury, CantAttack, \
    SpellDamage, DoubleDeathrattle, IncreaseWeaponAttack
import hearthbreaker.targeting
import copy
from hearthbreaker.cards.spells.neutral import ArmorPlating, EmergencyCoolant, FinickyCloakfield, TimeRewinder,\
    ReversingSwitch, RustyHorn, WhirlingBlades


class BloodfenRaptor(MinionCard):
    def __init__(self):
        super().__init__("Bloodfen Raptor", 2, CHARACTER_CLASS.ALL, CARD_RARITY.FREE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(3, 2)


class ElvenArcher(MinionCard):
    def __init__(self):
        super().__init__("Elven Archer", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Damage(1), CharacterSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(1, 1)


class NoviceEngineer(MinionCard):
    def __init__(self):
        super().__init__("Novice Engineer", 2, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         battlecry=Battlecry(Draw(), PlayerSelector()))

    def create_minion(self, player):
        return Minion(1, 1)


class StonetuskBoar(MinionCard):
    def __init__(self):
        super().__init__("Stonetusk Boar", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1, charge=True)


class IronbeakOwl(MinionCard):
    def __init__(self):
        super().__init__("Ironbeak Owl", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST,
                         battlecry=Battlecry(Silence(), MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(2, 1)


class WarGolem(MinionCard):
    def __init__(self):
        super().__init__("War Golem", 7, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(7, 7)


class MogushanWarden(MinionCard):
    def __init__(self):
        super().__init__("Mogu'shan Warden", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 7, taunt=True)


class FaerieDragon(MinionCard):
    def __init__(self):
        super().__init__("Faerie Dragon", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(3, 2, spell_targetable=False)


class KoboldGeomancer(MinionCard):
    def __init__(self):
        super().__init__("Kobold Geomancer", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 2, spell_damage=1)


class ArgentSquire(MinionCard):
    def __init__(self):
        super().__init__("Argent Squire", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 1, divine_shield=True)


class SilvermoonGuardian(MinionCard):
    def __init__(self):
        super().__init__("Silvermoon Guardian", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 3, divine_shield=True)


class TwilightDrake(MinionCard):
    def __init__(self):
        super().__init__("Twilight Drake", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(4, 1, battlecry=gain_one_health_for_each_card_in_hand)


class MagmaRager(MinionCard):
    def __init__(self):
        super().__init__("Magma Rager", 3, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(5, 1)


class DireWolfAlpha(MinionCard):
    def __init__(self):
        super().__init__("Dire Wolf Alpha", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 2, auras=[Aura(ChangeAttack(1), MinionSelector(Adjacent()))])


class WorgenInfiltrator(MinionCard):
    def __init__(self):
        super().__init__("Worgen Infiltrator", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 1, stealth=True)


class Archmage(MinionCard):
    def __init__(self):
        super().__init__("Archmage", 6, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 7, spell_damage=1)


class DalaranMage(MinionCard):
    def __init__(self):
        super().__init__("Dalaran Mage", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 4, spell_damage=1)


class Malygos(MinionCard):
    def __init__(self):
        super().__init__("Malygos", 9, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(4, 12, spell_damage=5)


class AzureDrake(MinionCard):
    def __init__(self):
        super().__init__("Azure Drake", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.DRAGON,
                         battlecry=Battlecry(Draw(), PlayerSelector()))

    def create_minion(self, player):
        return Minion(4, 4, spell_damage=1)


class OgreMagi(MinionCard):
    def __init__(self):
        super().__init__("Ogre Magi", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 4, spell_damage=1)


class Spellbreaker(MinionCard):
    def __init__(self):
        super().__init__("Spellbreaker", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.NONE,
                         battlecry=Battlecry(Silence(), MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(4, 3)


class BloodmageThalnos(MinionCard):
    def __init__(self):
        super().__init__("Bloodmage Thalnos", 2, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(1, 1, spell_damage=1, deathrattle=Deathrattle(Draw(), PlayerSelector()))


class LootHoarder(MinionCard):
    def __init__(self):
        super().__init__("Loot Hoarder", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 1, deathrattle=Deathrattle(Draw(), PlayerSelector()))


class LeperGnome(MinionCard):
    def __init__(self):
        super().__init__("Leper Gnome", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 1, deathrattle=Deathrattle(Damage(2), HeroSelector(EnemyPlayer())))


class IronforgeRifleman(MinionCard):
    def __init__(self):
        super().__init__("Ironforge Rifleman", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.NONE,
                         battlecry=Battlecry(Damage(1), CharacterSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(2, 2)


class GnomishInventor(MinionCard):
    def __init__(self):
        super().__init__("Gnomish Inventor", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Draw(), PlayerSelector()))

    def create_minion(self, player):
        return Minion(2, 4)


class GoldshireFootman(MinionCard):
    def __init__(self):
        super().__init__("Goldshire Footman", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 2, taunt=True)


class FrostwolfGrunt(MinionCard):
    def __init__(self):
        super().__init__("Frostwolf Grunt", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 2, taunt=True)


class IronfurGrizzly(MinionCard):
    def __init__(self):
        super().__init__("Ironfur Grizzly", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(3, 3, taunt=True)


class LordOfTheArena(MinionCard):
    def __init__(self):
        super().__init__("Lord of the Arena", 6, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(6, 5, taunt=True)


class MurlocRaider(MinionCard):
    def __init__(self):
        super().__init__("Murloc Raider", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(2, 1)


class ManaAddict(MinionCard):
    def __init__(self):
        super().__init__("Mana Addict", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 3, effects=[Effect(SpellCast(), Give(BuffUntil(ChangeAttack(2), TurnEnded())),
                                            SelfSelector())])


class OasisSnapjaw(MinionCard):
    def __init__(self):
        super().__init__("Oasis Snapjaw", 4, CHARACTER_CLASS.ALL, CARD_RARITY.FREE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 7)


class RecklessRocketeer(MinionCard):
    def __init__(self):
        super().__init__("Reckless Rocketeer", 6, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(5, 2, charge=True)


class RiverCrocolisk(MinionCard):
    def __init__(self):
        super().__init__("River Crocolisk", 2, CHARACTER_CLASS.ALL, CARD_RARITY.FREE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 3)


class SenjinShieldmasta(MinionCard):
    def __init__(self):
        super().__init__("Sen'jin Shieldmasta", 4, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(3, 5, taunt=True)


class ScarletCrusader(MinionCard):
    def __init__(self):
        super().__init__("Scarlet Crusader", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 1, divine_shield=True)


class Shieldbearer(MinionCard):
    def __init__(self):
        super().__init__("Shieldbearer", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(0, 4, taunt=True)


class SilverbackPatriarch(MinionCard):
    def __init__(self):
        super().__init__("Silverback Patriarch", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 4, taunt=True)


class JunglePanther(MinionCard):
    def __init__(self):
        super().__init__("Jungle Panther", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(4, 2, stealth=True)


class RavenholdtAssassin(MinionCard):
    def __init__(self):
        super().__init__("Ravenholdt Assassin", 7, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(7, 5, stealth=True)


class StormpikeCommando(MinionCard):
    def __init__(self):
        super().__init__("Stormpike Commando", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Damage(2), CharacterSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(4, 2)


class StormwindKnight(MinionCard):
    def __init__(self):
        super().__init__("Stormwind Knight", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 5, charge=True)


class StranglethornTiger(MinionCard):
    def __init__(self):
        super().__init__("Stranglethorn Tiger", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(5, 5, stealth=True)


class Sunwalker(MinionCard):
    def __init__(self):
        super().__init__("Sunwalker", 6, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(4, 5, divine_shield=True, taunt=True)


class ThrallmarFarseer(MinionCard):
    def __init__(self):
        super().__init__("Thrallmar Farseer", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, windfury=True)


class WindfuryHarpy(MinionCard):
    def __init__(self):
        super().__init__("Windfury Harpy", 6, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 5, windfury=True)


class YoungDragonhawk(MinionCard):
    def __init__(self):
        super().__init__("Young Dragonhawk", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1, windfury=True)


class Wolfrider(MinionCard):
    def __init__(self):
        super().__init__("Wolfrider", 3, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(3, 1, charge=True)


class BootyBayBodyguard(MinionCard):
    def __init__(self):
        super().__init__("Booty Bay Bodyguard", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(5, 4, taunt=True)


class BoulderfistOgre(MinionCard):
    def __init__(self):
        super().__init__("Boulderfist Ogre", 6, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(6, 7)


class ChillwindYeti(MinionCard):
    def __init__(self):
        super().__init__("Chillwind Yeti", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 5)


class CoreHound(MinionCard):
    def __init__(self):
        super().__init__("Core Hound", 7, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(9, 5)


class VoodooDoctor(MinionCard):
    def __init__(self):
        super().__init__("Voodoo Doctor", 1, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         battlecry=Battlecry(Heal(2), CharacterSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(2, 1)


class EarthenRingFarseer(MinionCard):
    def __init__(self):
        super().__init__("Earthen Ring Farseer", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Heal(3), CharacterSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(3, 3)


class ArcaneGolem(MinionCard):
    def __init__(self):
        super().__init__("Arcane Golem", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(GiveManaCrystal(), PlayerSelector(players=EnemyPlayer())))

    def create_minion(self, player):
        return Minion(4, 2, charge=True)


class PriestessOfElune(MinionCard):
    def __init__(self):
        super().__init__("Priestess of Elune", 6, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Heal(4), HeroSelector()))

    def create_minion(self, player):
        return Minion(5, 4)


class DarkscaleHealer(MinionCard):
    def __init__(self):
        super().__init__("Darkscale Healer", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Heal(2), CharacterSelector()))

    def create_minion(self, player):
        return Minion(4, 5)


class ArgentCommander(MinionCard):
    def __init__(self):
        super().__init__("Argent Commander", 6, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(4, 2, divine_shield=True, charge=True)


class BluegillWarrior(MinionCard):
    def __init__(self):
        super().__init__("Bluegill Warrior", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(2, 1, charge=True)


class Wisp(MinionCard):
    def __init__(self):
        super().__init__("Wisp", 0, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 1)


class Nightblade(MinionCard):
    def __init__(self):
        super().__init__("Nightblade", 5, CHARACTER_CLASS.ALL, CARD_RARITY.FREE,
                         battlecry=Battlecry(Damage(3), HeroSelector(EnemyPlayer())))

    def create_minion(self, player):
        return Minion(4, 4)


class ShatteredSunCleric(MinionCard):
    def __init__(self):
        super().__init__("Shattered Sun Cleric", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Give([Buff(ChangeAttack(1)), Buff(ChangeHealth(1))]),
                                             MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(3, 2)


class TheBlackKnight(MinionCard):
    def __init__(self):
        super().__init__("The Black Knight", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(Kill(), MinionSelector(HasStatus("taunt"), EnemyPlayer(), UserPicker())))

    def create_minion(self, player):
        return Minion(4, 5)


class AbusiveSergeant(MinionCard):
    def __init__(self):
        super().__init__("Abusive Sergeant", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Give(BuffUntil(ChangeAttack(2), TurnEnded(player=CurrentPlayer()))),
                                             MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(2, 1)


class DarkIronDwarf(MinionCard):
    def __init__(self):
        super().__init__("Dark Iron Dwarf", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Give(BuffUntil(ChangeAttack(2), TurnEnded(player=CurrentPlayer()))),
                                             MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(4, 4)


class Abomination(MinionCard):
    def __init__(self):
        super().__init__("Abomination", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(4, 4, deathrattle=Deathrattle(Damage(2), CharacterSelector(players=BothPlayer())), taunt=True)


class FenCreeper(MinionCard):
    def __init__(self):
        super().__init__("Fen Creeper", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 6, taunt=True)


class VentureCoMercenary(MinionCard):
    def __init__(self):
        super().__init__("Venture Co. Mercenary", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(7, 6, auras=[Aura(ManaChange(-3, 0, MinionCardSelector()), PlayerSelector())])


class AmaniBerserker(MinionCard):
    def __init__(self):
        super().__init__("Amani Berserker", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, enrage=Enrage(ChangeAttack(3), SelfSelector()))


class Squire(MinionCard):
    def __init__(self):
        super().__init__("Squire", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(2, 2)


class SilverHandKnight(MinionCard):
    def __init__(self):
        super().__init__("Silver Hand Knight", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Summon(Squire()), PlayerSelector()))

    def create_minion(self, player):
        return Minion(4, 4)


class StormwindChampion(MinionCard):
    def __init__(self):
        super().__init__("Stormwind Champion", 7, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(6, 6, auras=[Aura(ChangeAttack(1), MinionSelector()), Aura(ChangeHealth(1), MinionSelector())])


class Deathwing(MinionCard):
    def __init__(self):
        super().__init__("Deathwing", 10, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(12, 12, battlecry=deathwing)


class Alexstrasza(MinionCard):
    def __init__(self):
        super().__init__("Alexstrasza", 9, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON,
                         battlecry=Battlecry(SetHealth(15), HeroSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(8, 8)


class EmperorCobra(MinionCard):
    def __init__(self):
        super().__init__("Emperor Cobra", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 3, effects=[Effect(DidDamage(), Kill(), TargetSelector(IsMinion()))])


class CrazedAlchemist(MinionCard):
    def __init__(self):
        super().__init__("Crazed Alchemist", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         targeting_func=hearthbreaker.targeting.find_minion_battlecry_target)

    def create_minion(self, player):
        def swap(minion):
            if self.target is not None:
                temp_attack = self.target.calculate_attack()
                temp_health = self.target.health
                if temp_attack == 0:
                    self.target.die(None)
                else:
                    self.target.set_attack_to(temp_health)
                    self.target.set_health_to(temp_attack)
        return Minion(2, 2, battlecry=swap)


class AcidicSwampOoze(MinionCard):
    def __init__(self):
        super().__init__("Acidic Swamp Ooze", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        def destroy_enemy_weapon(player):
            if player.game.other_player.hero.weapon is not None:
                player.game.other_player.hero.weapon.destroy()
        return Minion(3, 2, battlecry=destroy_enemy_weapon)


class AncientBrewmaster(MinionCard):
    def __init__(self):
        super().__init__("Ancient Brewmaster", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Bounce(), MinionSelector(picker=UserPicker())))

    def create_minion(self, player):
        return Minion(5, 4)


class YouthfulBrewmaster(MinionCard):
    def __init__(self):
        super().__init__("Youthful Brewmaster", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Bounce(), MinionSelector(picker=UserPicker())))

    def create_minion(self, player):
        return Minion(3, 2)


class BaronGeddon(MinionCard):
    def __init__(self):
        super().__init__("Baron Geddon", 7, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(7, 5, effects=[Effect(TurnEnded(), Damage(2), CharacterSelector(players=BothPlayer()))])


class AngryChicken(MinionCard):
    def __init__(self):
        super().__init__("Angry Chicken", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1, enrage=Enrage(ChangeAttack(5), SelfSelector()))


class RagingWorgen(MinionCard):
    def __init__(self):
        super().__init__("Raging Worgen", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 3, enrage=Enrage([ChangeAttack(1), Windfury()], SelfSelector()))


class TaurenWarrior(MinionCard):
    def __init__(self):
        super().__init__("Tauren Warrior", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, taunt=True, enrage=Enrage(ChangeAttack(3), SelfSelector()))


class SpitefulSmith(MinionCard):
    def __init__(self):
        super().__init__("Spiteful Smith", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 6, enrage=Enrage(IncreaseWeaponAttack(2), WeaponSelector()))


class BloodKnight(MinionCard):
    def __init__(self):
        super().__init__("Blood Knight", 3, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        def collect_divine_shields(minion):
            shields_stolen = 0
            targets = hearthbreaker.targeting.find_minion_battlecry_target(player.game, lambda m: m.divine_shield)
            if targets is not None:
                for target in targets:
                    shields_stolen += 1
                    target.divine_shield = False
                for i in range(0, shields_stolen):
                    minion.increase_health(3)
                    minion.change_attack(3)
        return Minion(3, 3, battlecry=collect_divine_shields)


class FrostwolfWarlord(MinionCard):
    def __init__(self):
        super().__init__("Frostwolf Warlord", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        def buff_from_allies(minion):
            for i in range(0, len(minion.player.minions) - 1):
                minion.increase_health(1)
                minion.change_attack(1)
        return Minion(4, 4, battlecry=buff_from_allies)


class RaidLeader(MinionCard):
    def __init__(self):
        super().__init__("Raid Leader", 3, CHARACTER_CLASS.ALL, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(2, 2, auras=[Aura(ChangeAttack(1), MinionSelector())])


class MechanicalDragonling(MinionCard):
    def __init__(self):
        super().__init__("Mechanical Dragonling", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(2, 1)


class DragonlingMechanic(MinionCard):
    def __init__(self):
        super().__init__("Dragonling Mechanic", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Summon(MechanicalDragonling()), PlayerSelector()))

    def create_minion(self, player):
        return Minion(2, 4)


class MurlocScout(MinionCard):
    def __init__(self):
        super().__init__("Murloc Scout", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(1, 1)


class MurlocTidehunter(MinionCard):
    def __init__(self):
        super().__init__("Murloc Tidehunter", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MURLOC,
                         battlecry=Battlecry(Summon(MurlocScout()), PlayerSelector()))

    def create_minion(self, player):
        return Minion(2, 1)


class Boar(MinionCard):
    def __init__(self):
        super().__init__("Boar", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1)


class RazorfenHunter(MinionCard):
    def __init__(self):
        super().__init__("Razorfen Hunter", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Summon(Boar()), PlayerSelector()))

    def create_minion(self, player):
        return Minion(2, 3)


class KnifeJuggler(MinionCard):
    def __init__(self):
        super().__init__("Knife Juggler", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(3, 2, effects=[Effect(AfterAdded(), Damage(1),
                                            CharacterSelector(players=EnemyPlayer(),
                                                              picker=RandomPicker(),
                                                              condition=None))])


class BaineBloodhoof(MinionCard):
    def __init__(self):
        super().__init__("Baine Bloodhoof", 4, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(4, 5)


class CairneBloodhoof(MinionCard):
    def __init__(self):
        super().__init__("Cairne Bloodhoof", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(4, 5, deathrattle=Deathrattle(Summon(BaineBloodhoof()), PlayerSelector()))


class DamagedGolem(MinionCard):
    def __init__(self):
        super().__init__("Damaged Golem", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(2, 1)


class HarvestGolem(MinionCard):
    def __init__(self):
        super().__init__("Harvest Golem", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(2, 3, deathrattle=Deathrattle(Summon(DamagedGolem()), PlayerSelector()))


class FinkleEinhorn(MinionCard):
    def __init__(self):
        super().__init__("Finkle Einhorn", 2, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(3, 3)


class TheBeast(MinionCard):
    def __init__(self):
        super().__init__("The Beast", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(9, 7, deathrattle=Deathrattle(Summon(FinkleEinhorn()), PlayerSelector(EnemyPlayer())))


class SylvanasWindrunner(MinionCard):
    def __init__(self):
        super().__init__("Sylvanas Windrunner", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(5, 5, deathrattle=Deathrattle(Steal(), MinionSelector(players=EnemyPlayer(),
                                                                            picker=RandomPicker())))


class StampedingKodo(MinionCard):
    def __init__(self):
        super().__init__("Stampeding Kodo", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.BEAST,
                         battlecry=Battlecry(Kill(), MinionSelector(AttackLessThanOrEqualTo(2), EnemyPlayer(),
                                                                    RandomPicker())))

    def create_minion(self, player):
        return Minion(3, 5)


class FrostElemental(MinionCard):
    def __init__(self):
        super().__init__("Frost Elemental", 6, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Freeze(), CharacterSelector(players=BothPlayer())))

    def create_minion(self, player):
        return Minion(5, 5)


class Demolisher(MinionCard):
    def __init__(self):
        super().__init__("Demolisher", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 4, effects=[Effect(TurnStarted(), Damage(2),
                                            CharacterSelector(players=EnemyPlayer(), picker=RandomPicker()))])


class Doomsayer(MinionCard):
    def __init__(self):
        super().__init__("Doomsayer", 2, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(0, 7, effects=[Effect(TurnStarted(), Kill(),
                                            MinionSelector(condition=None, players=BothPlayer()))])


class Gruul(MinionCard):
    def __init__(self):
        super().__init__("Gruul", 8, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(7, 7, effects=[Effect(TurnEnded(player=BothPlayer()), ChangeAttack(1), SelfSelector()),
                                     Effect(TurnEnded(player=BothPlayer()), ChangeHealth(1), SelfSelector())])


class Gnoll(MinionCard):
    def __init__(self):
        super().__init__("Gnoll", 2, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(2, 2, taunt=True)


class Hogger(MinionCard):
    def __init__(self):
        super().__init__("Hogger", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(4, 4, effects=[Effect(TurnEnded(), Summon(Gnoll()), PlayerSelector())])


class Imp(MinionCard):
    def __init__(self):
        super().__init__("Imp", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(1, 1)


class ImpMaster(MinionCard):
    def __init__(self):
        super().__init__("Imp Master", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 5, effects=[Effect(TurnEnded(), Damage(1), SelfSelector()),
                                     Effect(TurnEnded(), Summon(Imp()), PlayerSelector())])


class InjuredBlademaster(MinionCard):
    def __init__(self):
        super().__init__("Injured Blademaster", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Damage(4), SelfSelector()))

    def create_minion(self, player):
        return Minion(4, 7)


class MasterSwordsmith(MinionCard):
    def __init__(self):
        super().__init__("Master Swordsmith", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 3, effects=[Effect(TurnEnded(), ChangeAttack(1), MinionSelector(picker=RandomPicker()))])


class NatPagle(MinionCard):
    def __init__(self):
        super().__init__("Nat Pagle", 2, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(0, 4, effects=[Effect(TurnStarted(), Draw(), PlayerSelector(), OneIn(2))])


class Nozdormu(MinionCard):
    def __init__(self):
        super().__init__("Nozdormu", 9, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON)

    def create_minion(self, player):             # Strictly worse than Alexstrasza
        return Minion(8, 8)                      # Is the effect even applicable to AI?


class RagnarosTheFirelord(MinionCard):
    def __init__(self):
        super().__init__("Ragnaros the Firelord", 8, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(8, 8, effects=[Effect(TurnEnded(), Damage(8),
                                            CharacterSelector(players=EnemyPlayer(), picker=RandomPicker()))],
                      buffs=[Buff(CantAttack())])


class AncientWatcher(MinionCard):
    def __init__(self):
        super().__init__("Ancient Watcher", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(4, 5, buffs=[Buff(CantAttack())])


class ColdlightOracle(MinionCard):
    def __init__(self):
        super().__init__("Coldlight Oracle", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.MURLOC,
                         battlecry=Battlecry(Draw(2), PlayerSelector(players=BothPlayer())))

    def create_minion(self, player):
        return Minion(2, 2)


class ColdlightSeer(MinionCard):
    def __init__(self):
        super().__init__("Coldlight Seer", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.MURLOC,
                         battlecry=Battlecry(Give(ChangeHealth(2)),
                                             MinionSelector(IsType(MINION_TYPE.MURLOC), BothPlayer())))

    def create_minion(self, player):
        return Minion(2, 3)


class GrimscaleOracle(MinionCard):
    def __init__(self):
        super().__init__("Grimscale Oracle", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(1, 1, auras=[Aura(ChangeAttack(1),
                                        MinionSelector(IsType(MINION_TYPE.MURLOC), BothPlayer()))])


class MurlocWarleader(MinionCard):
    def __init__(self):
        super().__init__("Murloc Warleader", 3, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(3, 3, auras=[Aura(ChangeAttack(2),
                                        MinionSelector(IsType(MINION_TYPE.MURLOC), BothPlayer())),
                                   Aura(ChangeHealth(1),
                                        MinionSelector(IsType(MINION_TYPE.MURLOC), BothPlayer()))])


class BigGameHunter(MinionCard):
    def __init__(self):
        super().__init__("Big Game Hunter", 3, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC,
                         battlecry=Battlecry(Kill(), MinionSelector(AttackGreaterThan(6), BothPlayer())))

    def create_minion(self, player):
        return Minion(4, 2)


class BloodsailCorsair(MinionCard):
    def __init__(self):
        super().__init__("Bloodsail Corsair", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        def reduce_durability(m):
            if player.game.other_player.hero.weapon is not None:
                if player.game.other_player.hero.weapon.durability > 1:
                    player.game.other_player.hero.weapon.durability -= 1
                else:
                    player.game.other_player.hero.weapon.destroy()

        return Minion(1, 2, battlecry=reduce_durability)


class BloodsailRaider(MinionCard):
    def __init__(self):
        super().__init__("Bloodsail Raider", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        def gain_weapon_attack(m):
            if player.hero.weapon is not None:
                m.change_attack(player.hero.weapon.base_attack)

        return Minion(2, 3, battlecry=gain_weapon_attack)


class CaptainGreenskin(MinionCard):
    def __init__(self):
        super().__init__("Captain Greenskin", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        def buff_weapon(m):
            if player.hero.weapon is not None:
                player.hero.weapon.base_attack += 1
                player.hero.weapon.durability += 1

        return Minion(5, 4, battlecry=buff_weapon)


class HungryCrab(MinionCard):
    def __init__(self):
        super().__init__("Hungry Crab", 1, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.BEAST,
                         hearthbreaker.targeting.find_minion_battlecry_target,
                         lambda minion: minion.card.minion_type is MINION_TYPE.MURLOC)

    def create_minion(self, player):
        def devour_murloc(m):
            if m.card.target is not None:
                m.card.target.die(None)
                m.change_attack(2)
                m.increase_health(2)

        return Minion(1, 2, battlecry=devour_murloc)


class MadBomber(MinionCard):
    def __init__(self):
        super().__init__("Mad Bomber", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON,
                         battlecry=Battlecry(Damage(1), CharacterSelector(players=BothPlayer(),
                                                                          picker=RandomPicker(3))))

    def create_minion(self, player):
        return Minion(3, 2)


class ManaWraith(MinionCard):
    def __init__(self):
        super().__init__("Mana Wraith", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(2, 2, auras=[Aura(ManaChange(-1, 0, MinionCardSelector()), PlayerSelector(players=BothPlayer()))])


class MindControlTech(MinionCard):
    def __init__(self):
        super().__init__("Mind Control Tech", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Steal(),
                                             MinionSelector(players=EnemyPlayer(), condition=None,
                                                            picker=RandomPicker()), OpponentMinionCountIsGreaterThan(3))
                         )

    def create_minion(self, player):
        return Minion(3, 3)


class MurlocTidecaller(MinionCard):
    def __init__(self):
        super().__init__("Murloc Tidecaller", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(1, 2, effects=[(Effect(MinionSummoned(IsType(MINION_TYPE.MURLOC), player=BothPlayer()),
                                             ChangeAttack(1), SelfSelector()))])


class Onyxia(MinionCard):
    def __init__(self):
        super().__init__("Onyxia", 9, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON,
                         battlecry=Battlecry(Summon(Whelp(), 6), PlayerSelector()))

    def create_minion(self, player):
        return Minion(8, 8)


class Whelp(MinionCard):
    def __init__(self):
        super().__init__("Whelp", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(1, 1)


class SouthseaCaptain(MinionCard):
    def __init__(self):
        super().__init__("Southsea Captain", 3, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        return Minion(3, 3, auras=[Aura(ChangeAttack(1), MinionSelector(IsType(MINION_TYPE.PIRATE))),
                                   Aura(ChangeHealth(1), MinionSelector(IsType(MINION_TYPE.PIRATE)))])


class SouthseaDeckhand(MinionCard):
    def __init__(self):
        super().__init__("Southsea Deckhand", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        def charge_if_weapon(m):
            if player.hero.weapon is not None:
                m.add_buff(Buff(Charge()))

        return Minion(2, 1, battlecry=charge_if_weapon)


class YoungPriestess(MinionCard):
    def __init__(self):
        super().__init__("Young Priestess", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(2, 1, effects=[Effect(TurnEnded(), ChangeHealth(1), MinionSelector(picker=RandomPicker()))])


class AcolyteOfPain(MinionCard):
    def __init__(self):
        super().__init__("Acolyte of Pain", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 3, effects=[Effect(Damaged(), Draw(), PlayerSelector())])


class CultMaster(MinionCard):
    def __init__(self):
        super().__init__("Cult Master", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 2, effects=[Effect(MinionDied(), Draw(), PlayerSelector())])


class Secretkeeper(MinionCard):
    def __init__(self):
        super().__init__("Secretkeeper", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 2, effects=[Effect(SpellCast(IsSecret(), BothPlayer()), ChangeAttack(1), SelfSelector()),
                                     Effect(SpellCast(IsSecret(), BothPlayer()), ChangeHealth(1), SelfSelector())])


class VioletApprentice(MinionCard):
    def __init__(self):
        super().__init__("Violet Apprentice", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(1, 1)


class VioletTeacher(MinionCard):
    def __init__(self):
        super().__init__("Violet Teacher", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(3, 5, effects=[Effect(SpellCast(), Summon(VioletApprentice()), PlayerSelector())])


class GadgetzanAuctioneer(MinionCard):
    def __init__(self):
        super().__init__("Gadgetzan Auctioneer", 6, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(4, 4, effects=[Effect(SpellCast(), Draw(), PlayerSelector())])


class FlameOfAzzinoth(MinionCard):
    def __init__(self):
        super().__init__("Flame of Azzinoth", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(2, 1)


class IllidanStormrage(MinionCard):
    def __init__(self):
        super().__init__("Illidan Stormrage", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DEMON)

    def create_minion(self, player):
        return Minion(7, 5, effects=[Effect(CardUsed(), Summon(FlameOfAzzinoth()), PlayerSelector())])


class FlesheatingGhoul(MinionCard):
    def __init__(self):
        super().__init__("Flesheating Ghoul", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, effects=[Effect(MinionDied(player=BothPlayer()), ChangeAttack(1), SelfSelector())])


class Lightwarden(MinionCard):
    def __init__(self):
        super().__init__("Lightwarden", 1, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 2, effects=[Effect(CharacterHealed(player=BothPlayer()), ChangeAttack(2), SelfSelector())])


class QuestingAdventurer(MinionCard):
    def __init__(self):
        super().__init__("Questing Adventurer", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(2, 2, effects=[Effect(CardPlayed(), ChangeAttack(1), SelfSelector()),
                                     Effect(CardPlayed(), ChangeHealth(1), SelfSelector())])


class GurubashiBerserker(MinionCard):
    def __init__(self):
        super().__init__("Gurubashi Berserker", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 7, effects=[
            Effect(CharacterDamaged(condition=MinionIsTarget()), ChangeAttack(3), SelfSelector())])


class AncientMage(MinionCard):
    def __init__(self):
        super().__init__("Ancient Mage", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Give(SpellDamage(1)), MinionSelector(condition=Adjacent())))

    def create_minion(self, player):
        return Minion(2, 5)


class DefenderOfArgus(MinionCard):
    def __init__(self):
        super().__init__("Defender of Argus", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Give([
                             Buff(Taunt()),
                             Buff(ChangeAttack(1)),
                             Buff(ChangeHealth(1))
                         ]), MinionSelector(Adjacent())))

    def create_minion(self, player):
        return Minion(2, 3)


class SunfuryProtector(MinionCard):
    def __init__(self):
        super().__init__("Sunfury Protector", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Give(Buff(Taunt())), MinionSelector(Adjacent())))

    def create_minion(self, player):
        return Minion(2, 3)


class HarrisonJones(MinionCard):
    def __init__(self):
        super().__init__("Harrison Jones", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        def destroy_enemy_weapon(m):
            if player.game.other_player.hero.weapon is not None:
                for i in range(0, player.game.other_player.hero.weapon.durability):
                    m.player.draw()
                m.player.game.other_player.hero.weapon.destroy()

        return Minion(5, 4, battlecry=destroy_enemy_weapon)


class Bananas(Card):
    def __init__(self):
        super().__init__("Bananas", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.change_attack(1)
        self.target.increase_health(1)


class KingMukla(MinionCard):
    def __init__(self):
        super().__init__("King Mukla", 3, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.BEAST,
                         battlecry=Battlecry(AddCard(Bananas(), 2), PlayerSelector(EnemyPlayer())))

    def create_minion(self, player):
        return Minion(5, 5)


class LeeroyJenkins(MinionCard):
    def __init__(self):
        super().__init__("Leeroy Jenkins", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(Summon(Whelp(), 2), PlayerSelector(players=EnemyPlayer())))

    def create_minion(self, player):
        return Minion(6, 2, charge=True)


class MountainGiant(MinionCard):
    def __init__(self):
        super().__init__("Mountain Giant", 12, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(8, 8)

    def mana_cost(self, player):
        cost = super().mana_cost(player) - len(player.hand)
        return cost


class MoltenGiant(MinionCard):
    def __init__(self):
        super().__init__("Molten Giant", 20, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(8, 8)

    def mana_cost(self, player):
        cost = super().mana_cost(player) - player.hero.calculate_max_health() + player.hero.health
        if cost < 0:
            return 0
        return cost


class SeaGiant(MinionCard):
    def __init__(self):
        super().__init__("Sea Giant", 10, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(8, 8)

    def mana_cost(self, player):
        cost = super().mana_cost(player) - len(player.game.players[0].minions) - len(player.game.players[1].minions)
        if cost < 0:
            return 0
        return cost


class DreadCorsair(MinionCard):
    def __init__(self):
        super().__init__("Dread Corsair", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        return Minion(3, 3, taunt=True)

    def mana_cost(self, player):
        if player.hero.weapon:
            cost = super().mana_cost(player) - player.hero.weapon.base_attack
        else:
            return 4
        if cost < 0:
            return 0
        return cost


class CaptainsParrot(MinionCard):
    def __init__(self):
        super().__init__("Captain's Parrot", 2, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.BEAST)

    def create_minion(self, player):
        def draw_pirate(m):
            if len(m.player.hand) < 10:
                card = m.game.random_draw(m.player.deck.cards,
                                          lambda c: not c.drawn and
                                          isinstance(c, MinionCard) and c.minion_type == MINION_TYPE.PIRATE)
                if card:
                    card.drawn = True
                    m.player.deck.left -= 1
                    m.player.hand.append(card)
                    m.player.trigger("card_drawn")

        return Minion(1, 1, battlecry=draw_pirate)


class TinkmasterOverspark(MinionCard):
    def __init__(self):
        super().__init__("Tinkmaster Overspark", 3, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        def transform_random(m):
            targets = copy.copy(player.game.other_player.minions)
            targets.extend(player.game.current_player.minions)
            targets.remove(m)
            if len(targets) > 0:
                target = player.game.random_choice(targets)
                choice = player.game.random_choice([Devilsaur(), Squirrel()])
                minion = choice.create_minion(None)
                minion.card = choice
                target.replace(minion)
        return Minion(3, 3, battlecry=transform_random)


class Squirrel(MinionCard):
    def __init__(self):
        super().__init__("Squirrel", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1)


class Devilsaur(MinionCard):
    def __init__(self):
        super().__init__("Devilsaur", 5, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(5, 5)


class AlarmoBot(MinionCard):
    def __init__(self):
        super().__init__("Alarm-o-Bot", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 3, effects=[Effect(TurnStarted(), SwapWithHand(), PlayerSelector())])


class IAmMurloc(Card):
    def __init__(self):
        super().__init__("I Am Murloc", 4, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def use(self, player, game):
        super().use(player, game)

        for i in range(0, player.game.random_amount(3, 5)):
            Murloc().summon(player, player.game, len(player.minions))


class PowerOfTheHorde(Card):
    def __init__(self):
        super().__init__("Power of the Horde", 4, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def use(self, player, game):
        super().use(player, game)

        horde_list = [FrostwolfGrunt(), TaurenWarrior(), ThrallmarFarseer(),
                      SilvermoonGuardian(), SenjinShieldmasta(), CairneBloodhoof()]
        horde_summon = game.random_choice(horde_list)
        horde_summon.summon(player, player.game, len(player.minions))


class RoguesDoIt(Card):
    def __init__(self):
        super().__init__("Rogues Do It...", 4, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL,
                         hearthbreaker.targeting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)

        self.target.damage(player.effective_spell_damage(4), self)
        player.draw()


class EliteTaurenChieftain(MinionCard):
    def __init__(self):
        super().__init__("Elite Tauren Chieftain", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(AddCard(CardQuery(source=CARD_SOURCE.LIST,
                                                               source_list=[IAmMurloc(),
                                                                            PowerOfTheHorde(),
                                                                            RoguesDoIt()])),
                                             PlayerSelector(BothPlayer())))

    def create_minion(self, player):
        return Minion(5, 5)


class Murloc(MinionCard):
    def __init__(self):
        super().__init__("Murloc", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MURLOC)

    def create_minion(self, p):
        return Minion(1, 1)


class MillhouseManastorm(MinionCard):
    def __init__(self):
        super().__init__("Millhouse Manastorm", 2, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(GiveEffect(Effect(TurnStarted(),
                                                               GiveAura(ManaAura(100, 0, SpellSelector(), False, True)),
                                                               PlayerSelector())), PlayerSelector(EnemyPlayer())))

    def create_minion(self, player):
        return Minion(4, 4)


class PintSizedSummoner(MinionCard):
    def __init__(self):
        super().__init__("Pint-Sized Summoner", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(2, 2, effects=[Effect(TurnStarted(), GiveAura(ManaAura(1, 0, MinionCardSelector(), True, True)),
                                            PlayerSelector())])


class OldMurkEye(MinionCard):
    def __init__(self):
        super().__init__("Old Murk-Eye", 4, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.MURLOC,
                         battlecry=Battlecry(Give(ChangeAttack(MinionSelector(IsType(MINION_TYPE.MURLOC),
                                                                              BothPlayer()))), SelfSelector()))

    def create_minion(self, player):
        return Minion(2, 4, charge=True,
                      effects=[Effect(MinionPlaced(condition=IsType(MINION_TYPE.MURLOC), player=BothPlayer()),
                                      ChangeAttack(1), SelfSelector()),
                               Effect(MinionDied(condition=IsType(MINION_TYPE.MURLOC), player=BothPlayer()),
                                      ChangeAttack(-1), SelfSelector())])


class Dream(Card):
    def __init__(self):
        super().__init__("Dream", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.bounce()


class YseraAwakens(Card):
    def __init__(self):
        super().__init__("Ysera Awakens", 2, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def use(self, player, game):
        super().use(player, game)
        targets = copy.copy(player.game.other_player.minions)
        targets.extend(player.game.current_player.minions)
        targets.append(player.game.other_player.hero)
        targets.append(player.game.current_player.hero)
        targets = filter(lambda m: not m.is_minion() or m.card.name != "Ysera", targets)
        for minion in targets:
            minion.damage(player.effective_spell_damage(5), self)


class Nightmare(Card):
    def __init__(self):
        super().__init__("Nightmare", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.add_buff(Buff(ChangeAttack(5)))
        self.target.add_buff(Buff(ChangeHealth(5)))
        self.target.add_effect(Effect(TurnStarted(), Kill(), SelfSelector()))


class LaughingSister(MinionCard):
    def __init__(self):
        super().__init__("Laughing Sister", 3, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(3, 5, spell_targetable=False)


class EmeraldDrake(MinionCard):
    def __init__(self):
        super().__init__("Emerald Drake", 4, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        return Minion(7, 6)


class Ysera(MinionCard):
    def __init__(self):
        super().__init__("Ysera", 9, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.DRAGON)

    def create_minion(self, player):
        dream_card_list = [EmeraldDrake(), LaughingSister(), Nightmare(), YseraAwakens(), Dream()]
        return Minion(4, 12, effects=[Effect(TurnEnded(),
                                             AddCard(CardQuery(source=CARD_SOURCE.LIST, source_list=dream_card_list)),
                                             PlayerSelector())])


class Chicken(MinionCard):
    def __init__(self):
        super().__init__("Chicken", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL,
                         MINION_TYPE.BEAST)

    def create_minion(self, p):
        return Minion(1, 1)


class GelbinMekkatorque(MinionCard):
    def __init__(self):
        super().__init__("Gelbin Mekkatorque", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        def awesome_invention(m):
            invention_list = [Emboldener3000(), HomingChicken(), Poultryizer(), RepairBot()]
            invention = player.game.random_choice(invention_list)
            invention.summon(player, player.game, m.index + 1)
        return Minion(6, 6, battlecry=awesome_invention)


class Emboldener3000(MinionCard):
    def __init__(self):
        super().__init__("Emboldener 3000", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 4, effects=[Effect(TurnEnded(), Give([Buff(ChangeAttack(1)),
                                                               Buff(ChangeHealth(1))]),
                                            MinionSelector(condition=None,
                                                           players=BothPlayer(),
                                                           picker=RandomPicker()))])


class HomingChicken(MinionCard):
    def __init__(self):
        super().__init__("Homing Chicken", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 3, effects=[Effect(TurnStarted(), Kill(), SelfSelector()),
                                     Effect(TurnStarted(), Draw(3), PlayerSelector())])


class Poultryizer(MinionCard):
    def __init__(self):
        super().__init__("Poultryizer", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 3, effects=[Effect(TurnStarted(), Transform(Chicken()),
                                            MinionSelector(None, BothPlayer(), RandomPicker()))])


class RepairBot(MinionCard):
    def __init__(self):
        super().__init__("Repair Bot", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 3, effects=[Effect(TurnEnded(), Heal(6),
                                            CharacterSelector(IsDamaged(), BothPlayer(), RandomPicker()))])


class LorewalkerCho(MinionCard):
    def __init__(self):
        super().__init__("Lorewalker Cho", 2, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(0, 4, effects=[Effect(SpellCast(player=BothPlayer()),
                                            AddCard(CardQuery(source=CARD_SOURCE.LAST_SPELL)),
                                            PlayerSelector(OtherPlayer()))])


class WildPyromancer(MinionCard):
    def __init__(self):
        super().__init__("Wild Pyromancer", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(3, 2, effects=[Effect(CardUsed(IsSpell()), Damage(1), MinionSelector(condition=None,
                                                                                           players=BothPlayer()))])


class FacelessManipulator(MinionCard):
    def __init__(self):
        super().__init__("Faceless Manipulator", 5, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC,
                         battlecry=Battlecry(Replace(), MinionSelector(players=BothPlayer(), picker=UserPicker())))

    def create_minion(self, player):
        return Minion(3, 3)


class Nerubian(MinionCard):
    def __init__(self):
        super().__init__("Nerubian", 3, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, p):
        return Minion(4, 4)


class NerubianEgg(MinionCard):
    def __init__(self):
        super().__init__("Nerubian Egg", 2, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(0, 2, deathrattle=Deathrattle(Summon(Nerubian()), PlayerSelector()))


class Maexxna(MinionCard):
    def __init__(self):
        super().__init__("Maexxna", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 8, effects=[Effect(DidDamage(), Kill(), TargetSelector(IsMinion()))])


class SpectralSpider(MinionCard):
    def __init__(self):
        super().__init__("Spectral Spider", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(1, 1)


class HauntedCreeper(MinionCard):
    def __init__(self):
        super().__init__("Haunted Creeper", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 2, deathrattle=Deathrattle(Summon(SpectralSpider(), 2), PlayerSelector()))


class NerubarWeblord(MinionCard):
    def __init__(self):
        super().__init__("Nerub'ar Weblord", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 4, auras=[Aura(ManaChange(-2, 0, BattlecrySelector()), PlayerSelector(BothPlayer()))])


class UnstableGhoul(MinionCard):
    def __init__(self):
        super().__init__("Unstable Ghoul", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 3, deathrattle=Deathrattle(Damage(1), MinionSelector(players=BothPlayer())), taunt=True)


class Loatheb(MinionCard):
    def __init__(self):
        super().__init__("Loatheb", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(GiveAura(ManaAura(-5, 0, SpellSelector(), False)),
                                             PlayerSelector(players=EnemyPlayer())))

    def create_minion(self, player):
        return Minion(5, 5)


class StoneskinGargoyle(MinionCard):
    def __init__(self):
        super().__init__("Stoneskin Gargoyle", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 4, effects=[Effect(TurnStarted(), Heal(10000), SelfSelector())])


class Slime(MinionCard):
    def __init__(self):
        super().__init__("Slime", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, p):
        return Minion(1, 2, taunt=True)


class SludgeBelcher(MinionCard):
    def __init__(self):
        super().__init__("Sludge Belcher", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(3, 5, taunt=True, deathrattle=Deathrattle(Summon(Slime()), PlayerSelector()))


class BaronRivendare(MinionCard):
    def __init__(self):
        super().__init__("Baron Rivendare", 4, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(1, 7, auras=[Aura(DoubleDeathrattle(), PlayerSelector())])


class DancingSwords(MinionCard):
    def __init__(self):
        super().__init__("Dancing Swords", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 4, deathrattle=Deathrattle(Draw(2), PlayerSelector(EnemyPlayer())))


class Deathlord(MinionCard):
    def __init__(self):
        super().__init__("Deathlord", 3, CHARACTER_CLASS.ALL, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(2, 8, taunt=True, deathrattle=Deathrattle(Summon(CardQuery(conditions=[IsMinion()],
                                                                                 source=CARD_SOURCE.MY_DECK)),
                                                                PlayerSelector(EnemyPlayer())))


class SpectralKnight(MinionCard):
    def __init__(self):
        super().__init__("Spectral Knight", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 6, spell_targetable=False)


class Undertaker(MinionCard):
    def __init__(self):
        super().__init__("Undertaker", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 2, effects=[Effect(MinionSummoned(MinionHasDeathrattle()), ChangeAttack(1), SelfSelector())])


class WailingSoul(MinionCard):
    def __init__(self):
        super().__init__("Wailing Soul", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Silence(), MinionSelector()))

    def create_minion(self, player):
        return Minion(3, 5)


class ZombieChow(MinionCard):
    def __init__(self):
        super().__init__("Zombie Chow", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, deathrattle=Deathrattle(Heal(5), HeroSelector(EnemyPlayer())))


class Thaddius(MinionCard):
    def __init__(self):
        super().__init__("Thaddius", 10, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL)

    def create_minion(self, player):
        return Minion(11, 11)


class Feugen(MinionCard):
    def __init__(self):
        super().__init__("Feugen", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(4, 7, deathrattle=Deathrattle(Summon(Thaddius()), PlayerSelector(), InGraveyard(Stalagg())))


class Stalagg(MinionCard):
    def __init__(self):
        super().__init__("Stalagg", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(7, 4, deathrattle=Deathrattle(Summon(Thaddius()), PlayerSelector(), InGraveyard(Feugen())))


class MadScientist(MinionCard):
    def __init__(self):
        super().__init__("Mad Scientist", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 2, deathrattle=Deathrattle(ApplySecret(CARD_SOURCE.MY_DECK), PlayerSelector()))


class EchoingOoze(MinionCard):
    def __init__(self):
        super().__init__("Echoing Ooze", 2, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        def duplicate_at_end(minion):
            player.add_effect(Effect(TurnEnded(), Duplicate(minion), PlayerSelector()))
        return Minion(1, 2, battlecry=duplicate_at_end)


class ShadeOfNaxxramas(MinionCard):
    def __init__(self):
        super().__init__("Shade of Naxxramas", 3, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(2, 2, stealth=True, effects=[Effect(TurnStarted(), ChangeAttack(1), SelfSelector()),
                                                   Effect(TurnStarted(), ChangeHealth(1), SelfSelector())])


class KelThuzad(MinionCard):
    def __init__(self):
        super().__init__("Kel'Thuzad", 8, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(6, 8, effects=[Effect(TurnEnded(player=BothPlayer()), ResurrectFriendly(), PlayerSelector())])


class PilotedShredder(MinionCard):
    def __init__(self):
        super().__init__("Piloted Shredder", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(4, 3, deathrattle=Deathrattle(Summon(CardQuery(conditions=[ManaCost(2), IsMinion()])),
                                                    PlayerSelector()))


class PilotedSkyGolem(MinionCard):
    def __init__(self):
        super().__init__("Piloted Sky Golem", 6, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(6, 4, deathrattle=Deathrattle(Summon(CardQuery(conditions=[ManaCost(4), IsMinion()])),
                                                    PlayerSelector()))


class SneedsOldShredder(MinionCard):
    def __init__(self):
        super().__init__("Sneed's Old Shredder", 8, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(5, 7, deathrattle=Deathrattle(Summon(CardQuery(conditions=[CardRarity(CARD_RARITY.LEGENDARY),
                                                                                 IsMinion()])),
                                                    PlayerSelector()))


class AntiqueHealbot(MinionCard):
    def __init__(self):
        super().__init__("Antique Healbot", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH,
                         battlecry=Battlecry(Heal(8), HeroSelector()))

    def create_minion(self, player):
        return Minion(3, 3)


class AnnoyOTron(MinionCard):
    def __init__(self):
        super().__init__("Annoy-o-Tron", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 2, divine_shield=True, taunt=True)


class ArcaneNullifierX21(MinionCard):
    def __init__(self):
        super().__init__("Arcane Nullifier X-21", 4, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(2, 5, taunt=True, spell_targetable=False)


class Blingtron3000(MinionCard):
    def __init__(self):
        super().__init__("Blingtron 3000", 5, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY, MINION_TYPE.MECH,
                         battlecry=Battlecry(Equip(CardQuery(conditions=[IsWeapon()])),
                                             PlayerSelector(players=BothPlayer())))

    def create_minion(self, player):
        return Minion(3, 4)


class BombLobber(MinionCard):
    def __init__(self):
        super().__init__("Bomb Lobber", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Damage(4), MinionSelector(None, EnemyPlayer(), RandomPicker())))

    def create_minion(self, player):
        return Minion(3, 3)


class BurlyRockjawTrogg(MinionCard):
    def __init__(self):
        super().__init__("Burly Rockjaw Trogg", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(3, 5, effects=[Effect(SpellCast(player=EnemyPlayer()), Give(ChangeAttack(2)), SelfSelector())])


class Mechwarper(MinionCard):
    def __init__(self):
        super().__init__("Mechwarper", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(2, 3, auras=[Aura(ManaChange(1, 0, MinionCardSelector(IsType(MINION_TYPE.MECH))),
                                        PlayerSelector())])


class Frog(MinionCard):
    def __init__(self):
        super().__init__("Frog", 0, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.BEAST)

    def create_minion(self, p):
        return Minion(0, 1, taunt=True)


class ClockworkGiant(MinionCard):
    def __init__(self):
        super().__init__("Clockwork Giant", 12, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(8, 8)

    def mana_cost(self, player):
        cost = super().mana_cost(player) - len(player.game.other_player.hand)
        return cost


spare_part_list = [ArmorPlating(), EmergencyCoolant(), FinickyCloakfield(), TimeRewinder(), ReversingSwitch(),
                   RustyHorn(), WhirlingBlades()]


class ClockworkGnome(MinionCard):
    def __init__(self):
        super().__init__("Clockwork Gnome", 1, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH)

    def create_minion(self, player):

        return Minion(2, 1,
                      deathrattle=Deathrattle(AddCard(CardQuery(source=CARD_SOURCE.LIST, source_list=spare_part_list)),
                                              PlayerSelector()))


class BoomBot(MinionCard):
    def __init__(self):
        super().__init__("Boom Bot", 1, CHARACTER_CLASS.ALL, CARD_RARITY.SPECIAL, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 1, deathrattle=Deathrattle(Damage(player.game.random_amount(1, 4)),
                                                    CharacterSelector(players=EnemyPlayer(), picker=RandomPicker())))


class DoctorBoom(MinionCard):
    def __init__(self):
        super().__init__("Dr. Boom", 7, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(Summon(BoomBot(), 2), PlayerSelector()))

    def create_minion(self, player):
        return Minion(7, 7)


class TargetDummy(MinionCard):
    def __init__(self):
        super().__init__("Target Dummy", 0, CHARACTER_CLASS.ALL, CARD_RARITY.RARE, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(0, 2, taunt=True)


class ExplosiveSheep(MinionCard):
    def __init__(self):
        super().__init__("Explosive Sheep", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 1, deathrattle=Deathrattle(Damage(2), CharacterSelector(players=BothPlayer())), taunt=True)


class Puddlestomper(MinionCard):
    def __init__(self):
        super().__init__("Puddlestomper", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MURLOC)

    def create_minion(self, player):
        return Minion(3, 2)


class MicroMachine(MinionCard):
    def __init__(self):
        super().__init__("Micro Machine", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 2, effects=[Effect(TurnStarted(player=BothPlayer()), ChangeAttack(1), SelfSelector())])


class MechanicalYeti(MinionCard):
    def __init__(self):
        super().__init__("Mechanical Yeti", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(4, 5,
                      deathrattle=Deathrattle(AddCard(CardQuery(source=CARD_SOURCE.LIST, source_list=spare_part_list)),
                                              PlayerSelector(BothPlayer())))


class SpiderTank(MinionCard):
    def __init__(self):
        super().__init__("Spider Tank", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(3, 4)


class GilblinStalker(MinionCard):
    def __init__(self):
        super().__init__("Gilblin Stalker", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, stealth=True)


class ShipsCannon(MinionCard):
    def __init__(self):
        super().__init__("Ship's Cannon", 2, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(2, 3, effects=[Effect(MinionSummoned(IsType(MINION_TYPE.PIRATE)), Damage(2),
                                            CharacterSelector(None, EnemyPlayer(), RandomPicker()))])


class OgreBrute(MinionCard):
    def __init__(self):
        super().__init__("Ogre Brute", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 4, effects=[Effect(Attack(), ChangeTarget(CharacterSelector(NotCurrentTarget(),
                                                                                     EnemyPlayer(),
                                                                                     RandomPicker())),
                                            SelfSelector(), OneIn(2))])


class MogorTheOgre(MinionCard):
    def __init__(self):
        super().__init__("Mogor the Ogre", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(7, 6, effects=[Effect(CharacterAttack(None, BothPlayer()), ChangeTarget(
            CharacterSelector(NotCurrentTarget(), EnemyPlayer(), RandomPicker())), TargetSelector(), OneIn(2))])


class Toshley(MinionCard):
    def __init__(self):
        super().__init__("Toshley", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY,
                         battlecry=Battlecry(AddCard(CardQuery(source=CARD_SOURCE.LIST, source_list=spare_part_list)),
                                             PlayerSelector()))

    def create_minion(self, player):
        return Minion(5, 7,
                      deathrattle=Deathrattle(AddCard(CardQuery(source=CARD_SOURCE.LIST, source_list=spare_part_list)),
                                              PlayerSelector()))


class ForceTankMAX(MinionCard):
    def __init__(self):
        super().__init__("Force-Tank MAX", 8, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(7, 7, divine_shield=True)


class FelReaver(MinionCard):
    def __init__(self):
        super().__init__("Fel Reaver", 5, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC, minion_type=MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(8, 8, effects=[Effect(CardPlayed(player=EnemyPlayer()),
                                            Discard(CardQuery(source=CARD_SOURCE.MY_DECK), 3), PlayerSelector())])


class MadderBomber(MinionCard):
    def __init__(self):
        super().__init__("Madder Bomber", 5, CHARACTER_CLASS.ALL, CARD_RARITY.RARE,
                         battlecry=Battlecry(Damage(1), CharacterSelector(players=BothPlayer(),
                                                                          picker=RandomPicker(6))))

    def create_minion(self, player):
        return Minion(5, 4)


class Gazlowe(MinionCard):
    def __init__(self):
        super().__init__("Gazlowe", 6, CHARACTER_CLASS.ALL, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(3, 6, effects=[Effect(SpellCast(ManaCost(1)),
                                            AddCard(CardQuery(conditions=[IsType(MINION_TYPE.MECH)])),
                                            PlayerSelector())])


class MiniMage(MinionCard):
    def __init__(self):
        super().__init__("Mini-Mage", 4, CHARACTER_CLASS.ALL, CARD_RARITY.EPIC)

    def create_minion(self, player):
        return Minion(4, 1, stealth=True, spell_damage=1)


class SaltyDog(MinionCard):
    def __init__(self):
        super().__init__("Salty Dog", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.PIRATE)

    def create_minion(self, player):
        return Minion(7, 4)


class GnomereganInfantry(MinionCard):
    def __init__(self):
        super().__init__("Gnomeregan Infantry", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(1, 4, charge=True, taunt=True)


class FlyingMachine(MinionCard):
    def __init__(self):
        super().__init__("Flying Machine", 3, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.MECH)

    def create_minion(self, player):
        return Minion(1, 4, windfury=True)


class LostTallstrider(MinionCard):
    def __init__(self):
        super().__init__("Lost Tallstrider", 4, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(5, 4)
