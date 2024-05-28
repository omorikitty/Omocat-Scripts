# -*- coding: utf-8 -*-
# coding: utf-8
from bsSpaz import *


# Agent Zoeeee
t = Appearance("EmpresariaPixie")
t.colorTexture = "agentColor"
t.colorMaskTexture = "agentColorMask"
t.defaultColor = (-6, -8, 5)

t.defaultHighlight = (4, 0, 0)
t.iconTexture = "star"
t.iconMaskTexture = "star"

t.headModel = "pixieHead"
t.torsoModel = "agentTorso"
t.pelvisModel = "agentPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel = "agentForeArm"
t.handModel = "agentHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel = "agentToes"

t.jumpSounds = ["warrior1", "warrior2", "warrior3"]
t.attackSounds = ["warrior1", "warrior2", "warrior3"]
t.impactSounds = [
    "warriorhit1",
    "warriorhit2",
]
t.deathSounds = ["warriorDeath", "warrior4"]
t.pickupSounds = ["warrior3"]
t.fallSounds = ["warriorDeath", "warrior4", "warriorFall"]

t.style = "agent"


# SANESSSS!!!
t = Appearance("astro")
t.colorTexture = "landMineLit"
t.colorMaskTexture = "landMineLit"
t.defaultColor = (1.0, 0.1, 1.2)

t.defaultHighlight = (0.16, 0.15, 2.4)
t.iconTexture = "landMineLit"
t.iconMaskTexture = "aliIconMask"

t.headModel = "bomb"
t.torsoModel = "cyborgPelvis"
t.pelvisModel = "cyborgPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel = "agentForeArm"
t.handModel = "cyborgHand"
t.upperLegModel = "cyborgUpperLeg"
t.lowerLegModel = "cyborgLowerLeg"
t.toesModel = "cyborgToes"

cyborgSounds =    ['cyborg1','cyborg2','cyborg3','cyborg4']
cyborgHitSounds = ['cyborgHit1','cyborgHit2']
t.attackSounds = cyborgSounds
t.jumpSounds = cyborgSounds
t.impactSounds = cyborgHitSounds
t.deathSounds=["cyborgDeath"]
t.pickupSounds = cyborgSounds
t.fallSounds=["cyborgFall"]
t.style = 'agent'


t = Appearance("BabySticky")

t.colorTexture = "bombStickyColor"
t.colorMaskTexture = "impactBombColorMask"

t.defaultColor = (0.3,0.3,0.3)
#t.defaultHighlight = (0.2,0.8,0.8)

t.iconTexture = "cuteSpazIcon"
t.iconMaskTexture = "cuteSpazIconMask"

t.headModel =     "bunnyPelvis"
t.torsoModel =    "bombSticky"
t.pelvisModel =   "bunnyPelvis"
t.upperArmModel = "bunnyPelvis"
t.foreArmModel =  "bunnyPelvis"
t.handModel =     "bunnyPelvis"
t.upperLegModel = "bunnyPelvis"
t.lowerLegModel = "bunnyPelvis"
t.toesModel =     "bunnyPelvis"
t.attackSounds = ['powerdown01']
t.jumpSounds = ['powerup01']
t.impactSounds = ["powerdown01"]
t.deathSounds=['powerdown01']
t.pickupSounds = ['ticking']
t.fallSounds=["powerdown01"]

t.style = 'pixie'

# SANESSSS!!!
t = Appearance("Bons")

t.colorTexture = "shield"
t.colorMaskTexture = "shield"

t.defaultColor = (1, 1, 1)
t.defaultHighlight = (0.55, 0.8, 0.55)

t.iconTexture = "shield"
t.iconMaskTexture = "bonesIconMask"

t.headModel = "bonesHead"
t.torsoModel = "cyborgTorso"
t.pelvisModel = "ninjaPelvis"
t.upperArmModel = "ninjaUpperArm"
t.foreArmModel = "ninjaForeArm"
t.handModel = "ninjaHand"
t.upperLegModel = "ninjaUpperLeg"
t.lowerLegModel = "ninjaLowerLeg"
t.toesModel = "ninjaToes"

bonesSounds =    ['bones1','bones2','bones3']
bonesHitSounds = ['bones1','bones2','bones3']

t.attackSounds = bonesSounds
t.jumpSounds = bonesSounds
t.impactSounds = bonesHitSounds
t.deathSounds=["bonesDeath"]
t.pickupSounds = bonesSounds
t.fallSounds=["bonesFall"]

t.style = 'bones'


# SANESSSS!!!
t = Appearance("DickMan")
t.colorTexture = "shield"
t.colorMaskTexture = "shield"
t.iconTexture = "santaIcon"
t.iconMaskTexture = "neoSpazIconMask"

t.headModel = "penguinTorso"
t.torsoModel = "santaTorso"
t.pelvisModel = "frostyHand"
t.upperArmModel = "frostyHand"
t.foreArmModel = "frostyHand"
t.handModel = "frostyHand"
t.upperLegModel = "frostyHand"
t.lowerLegModel = "frostyHand"
t.toesModel = "frostyPelvis"

t.jumpSounds = ninjaJumps
t.attackSounds = ninjaAttacks
t.impactSounds = ninjaHits
t.deathSounds = ["ninjaDeath1"]
t.pickupSounds = ninjaAttacks
t.fallSounds = ["ninjaFall1"]
t.style = 'bones'


###############  SPAZ   ##################
t = Appearance("Raphael")

t.colorTexture = "warriorColor"
t.colorMaskTexture = "warriorColorMask"
# 主要制作:Plasma Boson 致谢:寂寥长空
t.iconTexture = "warriorIcon"
t.iconMaskTexture = "warriorIconColorMask"

t.defaultColor = (0.55, 0.55, 0.55)
t.defaultHighlight = (0.5, 0.5, 0.5)

t.headModel = "warriorHead"
t.torsoModel = "warriorTorso"
t.pelvisModel = "warriorPelvis"
t.upperArmModel = "warriorUpperArm"
t.foreArmModel = "warriorForeArm"
t.handModel = "warriorHand"
t.upperLegModel = "warriorUpperLeg"
t.lowerLegModel = "warriorLowerLeg"
t.toesModel = "warriorToes"

t.jumpSounds = ["warrior1", "warrior2", "warrior3"]
t.attackSounds = ["warrior1", "warrior2", "warrior3"]
t.impactSounds = [
    "warriorhit1",
    "warriorhit2",
]
t.deathSounds = ["warriorDeath", "warrior4"]
t.pickupSounds = ["warrior3"]
t.fallSounds = ["warriorDeath", "warrior4", "warriorFall"]

t.style = 'agent'

###############  SPAZ   ##################
t = Appearance("Logicon")

t.colorTexture = "cyborgColor"
t.colorMaskTexture = "neoSpazColorMask"

t.defaultColor = (1, 0.5, 0)
t.defaultHighlight = (1, 1, 1)

t.iconTexture = "powerupCurse"
t.iconMaskTexture = "powerupCurseMask"

t.headModel = "cyborgHead"

t.torsoModel = "aliTorso"

t.pelvisModel = "aliPelvis"

t.upperArmModel = "aliUpperArm"
t.foreArmModel = "aliForeArm"
t.handModel = "aliHand"

t.upperLegModel = "aliUpperLeg"
t.lowerLegModel = "aliLowerLeg"
t.toesModel = "aliToes"

aliSounds = ['ali1', 'ali2', 'ali3', 'ali4']
aliHitSounds = ['aliHit1', 'aliHit2']

t.attackSounds = aliSounds
t.jumpSounds = aliSounds
t.impactSounds = aliHitSounds
t.deathSounds = ["aliDeath"]
t.pickupSounds = aliSounds
t.fallSounds = ["aliFall"]

t.style = 'ali'

##Created by BX-78##################
t = Appearance("Ninjazoe's")

t.colorTexture = "zoeColor"
t.colorMaskTexture = "zoeColorMask"

t.defaultColor = (0.6,0.6,0.6)
t.defaultHighlight = (0,1,0)

t.iconTexture = "zoeIcon"
t.iconMaskTexture = "zoeIconColorMask"

t.headModel = "zoeHead"
t.torsoModel = "ninjaTorso"
t.pelvisModel = "zoePelvis"
t.upperArmModel = "bearUpperArm"
t.foreArmModel = "bearForeArm"
t.handModel = "ninjaHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel = "agentToes"

t.jumpSounds=["zoeJump01",
              "zoeJump02",
              "zoeJump03"]
t.attackSounds=["zoeAttack01",
                "zoeAttack02",
                "zoeAttack03",
                "zoeAttack04"]
t.impactSounds=["zoeImpact01",
                "zoeImpact02",
                "zoeImpact03",
                "zoeImpact04"]
t.deathSounds=["zoeDeath01"]
t.pickupSounds=["zoePickup01"]
t.fallSounds=["zoeFall01"]

t.style = 'female'

t = Appearance("PixieMD")
t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"
t.defaultColor = (0.5,0.5,0.5)
t.defaultHighlight = (1,0,0)
t.iconTexture = "zoeIcon"
t.iconMaskTexture = "pixieIconColorMask"
t.headModel =     "pixieHead"
t.torsoModel =    "pixieTorso"
t.pelvisModel =   "pixiePelvis"
t.upperArmModel = "aliUpperArm"
t.foreArmModel =  "aliForeArm"
t.handModel =     "cyborgHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel =     "cyborgToes"
pixieSounds =    ['pixie1','pixie2','pixie3','pixie4']
pixieHitSounds = ['pixieHit1','pixieHit2']
t.attackSounds = pixieSounds
t.jumpSounds = frostySounds
t.impactSounds = penguinHitSounds
t.deathSounds=["pixieDeath"]
t.pickupSounds = pixieSounds
t.fallSounds=["penguinFall"]
t.style = 'pixie'


t = Appearance("PixieProLuci")

t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"

t.iconTexture = "pixieIcon"
t.iconMaskTexture = "pixieIconColorMask"

t.headModel = "pixieHead"
t.torsoModel = "pixieTorso"
t.pelvisModel = "pixiePelvis"
t.upperArmModel = "aliUpperArm"
t.foreArmModel = "aliForeArm"
t.handModel = "agentHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel = "pixieToes"

pixieSounds = ['pixie1', 'pixie2', 'pixie3', 'pixie4']
pixieHitSounds = ['pixieHit1', 'pixieHit2']
t.attackSounds = pixieSounds
t.jumpSounds = pixieSounds
t.impactSounds = pixieHitSounds
t.deathSounds = ["pixieDeath"]
t.pickupSounds = pixieSounds
t.fallSounds = ["pixieFall"]

t.style = 'pixie'

t = Appearance("SANESSSS")
t.colorTexture = "ninjaColor"
t.colorMaskTexture = "ninjaColorMask"
t.iconTexture = "egg2"
t.iconMaskTexture = "achievementTNT"

t.headModel = "ninjaHead"
t.torsoModel = "ninjaTorso"
t.pelvisModel = "ninjaPelvis"
t.upperArmModel = "pixiePelvis"
t.foreArmModel = "pixiePelvis"
t.handModel = "ninjaHand"
t.upperLegModel = "ninjaUpperLeg"
t.lowerLegModel = "ninjaLowerLeg"
t.toesModel = "pixiePelvis"


ninjaAttacks = ['ninjaAttack'+str(i+1)+'' for i in range(7)]
ninjaHits = ['ninjaHit'+str(i+1)+'' for i in range(8)]
ninjaJumps = ['ninjaAttack'+str(i+1)+'' for i in range(7)]

t.jumpSounds = ninjaJumps
t.attackSounds = ninjaAttacks
t.impactSounds = ninjaHits
t.deathSounds = ["ninjaDeath1"]
t.pickupSounds = ninjaAttacks
t.fallSounds = ["ninjaFall1"]
t.style = 'female'

# SANESSSS!!!
t = Appearance("SkullMan")
t.colorTexture = "powerupCurse"
t.colorMaskTexture = "powerupCurse"
t . defaultColor = (1.0, 0.1, 1.2)

t . defaultHighlight = (0.16, 0.15, 2.4)
t.iconTexture = "powerupCurse"
t.iconMaskTexture = "powerupCurse"

t.headModel = "bomb"
t.torsoModel = "ninjaTorso"
t.pelvisModel = "cyborgPelvis"
t.upperArmModel = "cyborgUpperArm"
t.foreArmModel = "cyborgForeArm"
t.handModel = "cyborgHand"
t.upperLegModel = "cyborgUpperLeg"
t.lowerLegModel = "cyborgLowerLeg"
t.toesModel = "cyborgToes"

cyborgSounds =    ['cyborg1','cyborg2','cyborg3','cyborg4']
cyborgHitSounds = ['cyborgHit1','cyborgHit2']
t.attackSounds = cyborgSounds
t.jumpSounds = cyborgSounds
t.impactSounds = cyborgHitSounds
t.deathSounds=["cyborgDeath"]
t.pickupSounds = cyborgSounds
t.fallSounds=["cyborgFall"]
t . style = 'agent'

# SANESSSS!!!
t = Appearance("SnowGuy")
t.colorTexture = "achievementFlawlessVictory"
t.colorMaskTexture = "achievementFlawlessVictory"
t . defaultColor = (1.0, 0.1, 1.2)

t . defaultHighlight = (0.16, 0.15, 2.4)
t.iconTexture = "achievementFlawlessVictory"
t.iconMaskTexture = "aliIconMask"

t.headModel = "aliHead"
t.torsoModel = "pixiePelvis"
t.pelvisModel = "pixiePelvis"
t.upperArmModel = "pixiePelvis"
t.foreArmModel = "pixiePelvis"
t.handModel = "pixiePelvis"
t.upperLegModel = "pixiePelvis"
t.lowerLegModel = "pixiePelvis"
t.toesModel = "pixiePelvis"

aliSounds =    ['ali1','ali2','ali3','ali4']
aliHitSounds = ['aliHit1','aliHit2']
t.attackSounds = aliSounds
t.jumpSounds = aliSounds
t.impactSounds = aliHitSounds
t.deathSounds=["aliDeath"]
t.pickupSounds = aliSounds
t.fallSounds=["aliFall"]
t . style = 'ali'

###############  SPAZ   ##################
t = Appearance("Sparky")

t.colorTexture = u"cowboyColor"
t.colorMaskTexture = u"cowboyColorMask"

t.iconTexture = u"cowboyIcon"
t.iconMaskTexture = u"cowboyIconColorMask"

t.defaultColor = (0.75, 0.75, 0.75)
t.defaultHighlight = (0.5, 0.5, 0.5)

t.headModel = "kronkHead"
t.torsoModel = "cyborgTorso"
t.pelvisModel = "ninjaPelvis"
t.upperArmModel = "bunnyUpperArm"
t.foreArmModel = "bunnyForeArm"
t.handModel = "zoeHand"
t.upperLegModel = "penguinUpperLeg"
t.lowerLegModel = "penguinLowerLeg"
t.toesModel = "pixieToes"

t.jumpSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.attackSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.impactSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.deathSounds = ["kronkDeath"]
t.pickupSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.fallSounds = ["kronkFall"]

t.style = 'agent'


###############  SPAZ   ##################
t = Appearance("Steve")

t.colorTexture = u"cowboyColor"
t.colorMaskTexture = u"cowboyColorMask"

t.iconTexture = u"cowboyIcon"
t.iconMaskTexture = u"cowboyIconColorMask"

t.defaultColor = (0.75, 0.75, 0.75)
t.defaultHighlight = (0.5, 0.5, 0.5)

t.headModel = "cowboyHead"
t.torsoModel = "cowboyTorso"
t.pelvisModel = "cowboyPelvis"
t.upperArmModel = "cowboyUpperArm"
t.foreArmModel = "cowboyForeArm"
t.handModel = "cowboyHand"
t.upperLegModel = "cowboyUpperLeg"
t.lowerLegModel = "cowboyLowerLeg"
t.toesModel = "cowboyToes"

t.jumpSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.attackSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.impactSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.deathSounds = ["kronkDeath"]
t.pickupSounds = [
    "kronk1", "kronk2", "kronk3", "kronk4", "kronk5", "kronk6", "kronk7",
    "kronk8", "kronk9", "kronk10"
]
t.fallSounds = ["kronkFall"]

t.style = 'agent'

# SANESSSS!!!
t = Appearance("XPixel")
t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"
t . defaultColor = (1.0, 0.1, 1.2)

t . defaultHighlight = (0.16, 0.15, 2.4)
t.iconTexture = "pixieIcon"
t.iconMaskTexture = "pixieIconColorMask"

t.headModel = "pixieHead"
t.torsoModel = "pixieTorso"
t.pelvisModel = "pixiePelvis"
t.upperArmModel = "pixiePelvis"
t.foreArmModel = "pixiePelvis"
t.handModel = "pixieHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel = "pixiePelvis"

pixieSounds = ['pixie1', 'pixie2', 'pixie3', 'pixie4']
pixieHitSounds = ['pixieHit1', 'pixieHit2']
t . attackSounds = pixieSounds
t . jumpSounds = pixieSounds
t . impactSounds = pixieHitSounds
t . deathSounds = ["pixieDeath"]
t . pickupSounds = pixieSounds
t . fallSounds = ["pixieFall"]
t . style = 'pixie'

# SANESSSS!!!
t = Appearance("ZPixel")
t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"
t . defaultColor = (1.0, 0.1, 1.2)

t . defaultHighlight = (0.16, 0.15, 2.4)
t.iconTexture = "zoeIcon"
t.iconMaskTexture = "pixieIconColorMask"

t.headModel = "pixieHead"
t.torsoModel = "pixieTorso"
t.pelvisModel = "pixiePelvis"
t.upperArmModel = "pixiePelvis"
t.foreArmModel = "pixiePelvis"
t.handModel = "pixieHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel = "pixiePelvis"

pixieSounds = ['pixie1', 'pixie2', 'pixie3', 'pixie4']
pixieHitSounds = ['pixieHit1', 'pixieHit2']
t . attackSounds = pixieSounds
t . jumpSounds = pixieSounds
t . impactSounds = pixieHitSounds
t . deathSounds = ["pixieDeath"]
t . pickupSounds = pixieSounds
t . fallSounds = ["pixieFall"]
t . style = 'female'

# Penguin Dude # Created by Friends
t = Appearance("Frosty Man")
t.colorTexture = "cyborgColor"
t.colorMaskTexture = "egg2"
t.iconTexture = "achievementInControl"
t.iconMaskTexture = "eggTex1"

t.headModel = "melTorso"
t.torsoModel = "aliTorso"
t.pelvisModel = "bunnyPelvis"
t.upperArmModel = "bunnyPelvis"
t.foreArmModel = "santaForeArm"
t.handModel = "santaHand"
t.upperLegModel = "bunnyPelvis"
t.lowerLegModel = "bunnyPelvis"
t.toesModel = "bunnyToes"

t.jumpSounds=["frostyJump01",
              "frostyJump02",
              "frostyJump03",
              "frostyJump04"]
t.attackSounds=["frostyAttack01",
                "frostyAttack02",
                "frostyAttack03",
                "frostyAttack04"]
t.impactSounds=["pixieImpact01",
                "pixieImpact02",
                "pixieImpact03",
                "pixielmpact04"]
t.deathSounds=["frostyDeath01"]
t.pickupSounds=["shatter"]
t.fallSounds=["frostyFall01"]

t.style = 'agent'