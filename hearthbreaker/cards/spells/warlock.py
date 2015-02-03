import copy
from hearthbreaker.tags.action import Kill
from hearthbreaker.tags.base import Effect
from hearthbreaker.tags.event import TurnStarted, TurnEnded
from hearthbreaker.tags.selector import SelfSelector, EnemyPlayer
import hearthbreaker.targeting
from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY, MINION_TYPE
from hearthbreaker.game_objects import Card, Minion, MinionCard, Hero
from hearthbreaker.cards.minions.warlock import Voidwalker, FlameImp, DreadInfernal, Succubus, Felguard, BloodImp


class MortalCoil(Card):
    def __init__(self):
        super().__init__("Mortal Coil", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        if self.target.health <= player.effective_spell_damage(1) and not self.target.divine_shield:
            self.target.damage(player.effective_spell_damage(1), self)
            player.draw()
        else:
            self.target.damage(player.effective_spell_damage(1), self)
            # not sure how necessary this is, making sure damage before
            # draw but need to compare health before dealing damage


class Hellfire(Card):
    def __init__(self):
        super().__init__("Hellfire", 4, CHARACTER_CLASS.WARLOCK, CARD_RARITY.FREE)

    def use(self, player, game):
        super().use(player, game)
        targets = copy.copy(game.other_player.minions)
        targets.extend(game.current_player.minions)
        targets.append(game.other_player.hero)
        targets.append(game.current_player.hero)
        for minion in targets:
            minion.damage(player.effective_spell_damage(3), self)


class ShadowBolt(Card):
    def __init__(self):
        super().__init__("Shadow Bolt", 3, CHARACTER_CLASS.WARLOCK, CARD_RARITY.FREE,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.damage(player.effective_spell_damage(4), self)


class DrainLife(Card):
    def __init__(self):
        super().__init__("Drain Life", 3, CHARACTER_CLASS.WARLOCK,
                         CARD_RARITY.FREE, hearthbreaker.targeting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.damage(player.effective_spell_damage(2), self)
        player.hero.heal(player.effective_heal_power(2), self)


class Soulfire(Card):
    def __init__(self):
        super().__init__("Soulfire", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.damage(player.effective_spell_damage(4), self)
        player.discard()


class TwistingNether(Card):
    def __init__(self):
        super().__init__("Twisting Nether", 8, CHARACTER_CLASS.WARLOCK, CARD_RARITY.EPIC)

    def use(self, player, game):
        super().use(player, game)
        targets = copy.copy(game.other_player.minions)
        targets.extend(game.current_player.minions)
        for minion in targets:
            minion.die(self)


class Demonfire(Card):
    def __init__(self):
        super().__init__("Demonfire", 2, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        targets = copy.copy(player.game.current_player.minions)
        if self.target.card.minion_type is MINION_TYPE.DEMON and self.target in targets:
            self.target.change_attack(2)
            self.target.increase_health(2)
        else:
            self.target.damage(player.effective_spell_damage(2), self)


class SacrificialPact(Card):
    def __init__(self):
        super().__init__("Sacrificial Pact", 0, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_spell_target,
                         lambda character: (isinstance(character, Minion)
                                            and character.card.minion_type is MINION_TYPE.DEMON)
                         or (isinstance(character, Hero)
                             and character.character_class is CHARACTER_CLASS.LORD_JARAXXUS))

    def use(self, player, game):
        super().use(player, game)
        self.target.die(self)
        player.hero.heal(player.effective_heal_power(5), self)


class SiphonSoul(Card):
    def __init__(self):
        super().__init__("Siphon Soul", 6, CHARACTER_CLASS.WARLOCK, CARD_RARITY.RARE,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.die(self)
        player.hero.heal(player.effective_heal_power(3), self)


class SenseDemons(Card):
    def __init__(self):
        super().__init__("Sense Demons", 3, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON)

    def use(self, player, game):
        super().use(player, game)

        for i in range(0, 2):
            demon_card = game.random_draw(game.current_player.deck.cards,
                                          lambda c: not c.drawn and
                                          isinstance(c, MinionCard) and
                                          c.minion_type == MINION_TYPE.DEMON)
            if demon_card:
                demon_card.drawn = True
                player.deck.left -= 1
                if len(player.hand) < 10:
                    player.hand.append(demon_card)
                    self.trigger("card_drawn", demon_card)
                else:
                    player.trigger("card_destroyed", demon_card)
            else:
                if len(player.hand) < 10:
                    player.hand.append(hearthbreaker.cards.minions.warlock.WorthlessImp())
                    self.trigger("card_drawn", hearthbreaker.cards.minions.warlock.WorthlessImp())


class BaneOfDoom(Card):
    def __init__(self):
        super().__init__("Bane of Doom", 5, CHARACTER_CLASS.WARLOCK, CARD_RARITY.EPIC,
                         hearthbreaker.targeting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        demon_list = [BloodImp, Voidwalker, FlameImp, DreadInfernal, Succubus, Felguard]
        card = game.random_choice(demon_list)
        if self.target.health <= player.effective_spell_damage(2) and \
                (isinstance(self.target, Minion) and not self.target.divine_shield):
            self.target.damage(player.effective_spell_damage(2), self)
            card().summon(player, game, len(player.minions))
        else:
            self.target.damage(player.effective_spell_damage(2), self)


class Shadowflame(Card):
    def __init__(self):
        super().__init__("Shadowflame", 4, CHARACTER_CLASS.WARLOCK, CARD_RARITY.RARE,
                         hearthbreaker.targeting.find_friendly_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        shadowflame_damage = self.target.calculate_attack()
        self.target.die(self)
        for minion in game.other_player.minions:
            minion.damage(player.effective_spell_damage(shadowflame_damage),
                          self)


class Corruption(Card):
    def __init__(self):
        super().__init__("Corruption", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_enemy_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.add_effect(Effect(TurnStarted(player=EnemyPlayer()), Kill(), SelfSelector()))


class PowerOverwhelming(Card):
    def __init__(self):
        super().__init__("Power Overwhelming", 1, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_friendly_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)

        self.target.add_effect(Effect(TurnEnded(), Kill(), SelfSelector()))
        self.target.change_attack(4)
        self.target.increase_health(4)


class Darkbomb(Card):
    def __init__(self):
        super().__init__("Darkbomb", 2, CHARACTER_CLASS.WARLOCK, CARD_RARITY.COMMON,
                         hearthbreaker.targeting.find_spell_target)

    def use(self, player, game):
        super().use(player, game)
        self.target.damage(player.effective_spell_damage(3), self)


class Demonheart(Card):
    def __init__(self):
        super().__init__("Demonheart", 5, CHARACTER_CLASS.WARLOCK, CARD_RARITY.EPIC,
                         hearthbreaker.targeting.find_minion_spell_target)

    def use(self, player, game):
        super().use(player, game)
        targets = copy.copy(player.game.current_player.minions)
        if self.target.card.minion_type is MINION_TYPE.DEMON and self.target in targets:
            self.target.change_attack(5)
            self.target.increase_health(5)
        else:
            self.target.damage(player.effective_spell_damage(5), self)
