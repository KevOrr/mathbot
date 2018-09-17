from discord.ext.commands import command

TIER_NONE = 0
TIER_CONSTANT = 1
TIER_QUADRATIC = 2
TIER_EXPONENTIAL = 3
TIER_SPECIAL = 4


class InvalidPatronRankError(Exception):
	pass


class PatronageMixin:

	def patron_tier(self, uid):
		if not isinstance(uid, (str, int)):
			raise TypeError('User ID looks invalid')
		rank_string = self.parameters.get('patrons').get(str(uid))
		if rank_string is None:
			return TIER_NONE
		elif rank_string.startswith('constant'):
			return TIER_CONSTANT
		elif rank_string.startswith('quadratic'):
			return TIER_QUADRATIC
		elif rank_string.startswith('exponential'):
			return TIER_EXPONENTIAL
		elif rank_string.startswith('special'):
			return TIER_SPECIAL
		raise InvalidPatronRankError
		# return self.keystore.get('patron', str(uid)) or 0


class PatronModule:

	def __init__(self, bot):
		self.bot = bot

	@command()
	async def check_patronage(self, ctx):
		tier = ctx.bot.patron_tier(ctx.author.id)
		await ctx.send(f'Your patronage tier is {get_tier_name(tier)}')

	async def on_ready(self):
		guild = self.bot.get_guild(233826358369845251)
		if guild is None:
			print('Could not get mathbot guild in order to find patrons')
		else:
			for member in guild.members:
				tier = max(role_to_tier(r.name) for r in members.roles)
				if tier != 0:
					print(member, 'is teir', get_tier_name(tier))
					self.bot.keystore.set('patron', str(member.id), tier, expire = 60 * 60 * 24 * 3)


def get_tier_name(tier):
	try:
		return {
			TIER_NONE: 'None',
			TIER_CONSTANT: 'Constant',
			TIER_QUADRATIC: 'Quadratic',
			TIER_EXPONENTIAL: 'Exponential',
			TIER_SPECIAL: 'Ackermann'
		}[tier]
	except KeyError:
		raise InvalidPatronRankError


def role_name_to_tier(name):
	return {
		'Constant': TIER_CONSTANT,
		'Quadratic': TIER_QUADRATIC,
		'Exponential': TIER_EXPONENTIAL,
		'Moderator': TIER_SPECIAL,
		'Developer': TIER_SPECIAL
	}.get(name, TIER_NONE)


def setup(bot):
	return bot.add_cog(PatronModule(bot))
