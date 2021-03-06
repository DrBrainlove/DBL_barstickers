import matplotlib
matplotlib.use('Agg')  # no displayed figures -- need to call before loading pylab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import defaultdict
import numpy as np
import re
import matplotlib.patheffects as PathEffects
import numpy.lib.recfunctions as recfunctions
from scipy.optimize import fmin_l_bfgs_b
from matplotlib import gridspec


np.random.seed(seed=1234)

outer_colors = np.random.permutation(matplotlib.colors.cnames.keys())

#figsize = (15,1.8)
figsize = (7,0.938)

# fontsize_big = 80
# fontsize_small = 32
fontsize_big = 42
fontsize_big_num = 46
fontsize_small = 18

def new_node_attributes():
	global outer_colors
	scl = 1.

	outer_colors = np.roll(outer_colors, -1)

	return {
		'color':outer_colors[0],
		}
node_attributes = defaultdict(new_node_attributes)

homophonic_node_names 	= set(['ABS', 'ABY', 'ACE', 'ACT', 'ADD', 'ADO', 'ADS', 'AFT', 'AGE', 'AGO', 'AID', 'AIL', 'AIM', 'AIR', 'ALE', 'ALL', 'AMP', 'AND', 'ANT', 'ANY', 'APE', 'APT', 'ARC', 'ARE', 'ARK', 'ARM', 'ART', 'ASK', 'ASP', 'ASS', 'COP', 'COT', 'COW', 'COY', 'CRY', 'CUB', 'CUE', 'CUP', 'CUT', 'DAB', 'DAD', 'DAY', 'DEN', 'DEW', 'DIB', 'DID', 'DIE', 'DIG', 'DIM', 'DIN', 'DIP', 'DOE', 'DOG', 'DOT', 'DRY', 'DUB', 'DUD', 'DUE', 'DUG', 'DUH', 'GET', 'GIG', 'GIN', 'GIT', 'GNU', 'GOO', 'GOT', 'GUM', 'GUN', 'GUT', 'GUY', 'GYM', 'HAD', 'HAM', 'HAS', 'HAT', 'HAY', 'HEM', 'HEN', 'HER', 'HEW', 'HEX', 'HEY', 'HID', 'HIM', 'HIP', 'HIS', 'HIT', 'HOE', 'HOG', 'LID', 'LIE', 'LIP', 'LIT', 'LOB', 'LOG', 'LOO', 'LOP', 'LOT', 'LOW', 'LUG', 'LYE', 'MAC', 'MAD', 'MAG', 'MAN', 'MAP', 'MAR', 'MAT', 'MAW', 'MAX', 'MAY', 'MEN', 'MET', 'MIC', 'MID', 'MIT', 'MIX', 'MOB', 'MOD', 'PEN', 'PET', 'PEW', 'PIC', 'PIE', 'PIG', 'PIN', 'PIT', 'PIX', 'PLY', 'POD', 'POI', 'POP', 'POT', 'POW', 'PRO', 'PRY', 'PUB', 'PUG', 'PUN', 'PUP', 'PUT', 'QUO', 'RAD', 'RAG', 'RAM', 'RAN', 'RAP', 'RAT', 'SUP', 'TAB', 'TAD', 'TAG', 'TAN', 'TAP', 'TAR', 'TAT', 'TAX', 'TEA', 'TEE', 'TEN', 'THE', 'TIC', 'TIE', 'TIL', 'TIN', 'TIP', 'TOE', 'TOM', 'TOO', 'TOP', 'TOT', 'TOW', 'TOY', 'TRY', 'TUB', 'TUG', 'TWO',])
new_node_names 			= set(['ACE', 'ACT', 'ADO', 'AGE', 'AGO', 'AHI', 'AIM', 'AIR', 'ALA', 'ALL', 'AMP', 'ARM', 'ART', 'ASH', 'ASK', 'BAH', 'BAM', 'BAR', 'BED', 'BIO', 'BOA', 'BOX', 'BOY', 'BRO', 'BUG', 'CAB', 'CHI', 'CIS', 'COW', 'COP', 'CUP', 'COY', 'DAD', 'DAY', 'DIG', 'DOG', 'DRY', 'DUB', 'DUH', 'DUI', 'EAR', 'EGG', 'EGO', 'ELF', 'ELK', 'EON', 'ERA', 'ETA', 'EVE', 'EYE', 'FAN', 'FAX', 'FEW', 'FIG', 'FIX', 'FLU', 'FLY', 'FOG', 'FOR', 'FOX', 'FRO', 'FUN', 'GAL', 'GAS', 'GEL', 'GET', 'GIG', 'GIN', 'GOO', 'GUN', 'GUT', 'GYM', 'HAM', 'HAY', 'HEX', 'HIP', 'HIT', 'HOT', 'HOW', 'HUG', 'ICE', 'INK', 'IRE', 'IVY', 'JAM', 'JAR', 'JOB', 'JOY', 'JUG', 'KEG', 'KEY', 'KIT', 'LAB', 'LAM', 'LAW', 'LAX', 'LEG', 'LID', 'LIE', 'LUG', 'MAC', 'MAD', 'MAY', 'MIX', 'MOM', 'MOO', 'MOP', 'NAN', 'NAY', 'NIX', 'NIL', 'NEW', 'NOM', 'NOR', 'OAK', 'OAR', 'ODD', 'OFF', 'OIL', 'OLD', 'ONO', 'ORC', 'OVA', 'PAW', 'PAY', 'PHI', 'PIE', 'PIG', 'PLY', 'POP', 'PRO', 'RAD', 'RAW', 'REF', 'RIB', 'ROB', 'RUG', 'RUM', 'SAD', 'SAW', 'SAY', 'SEX', 'SHY', 'SIP', 'SIR', 'SKY', 'SOY', 'SPY', 'SUN', 'TAG', 'TAU', 'TAR', 'TAX', 'TAT', 'TOY', 'TRY', 'TUB', 'TUX', 'USE', 'VAN', 'VOW', 'WAR', 'WAS', 'WAX', 'WET', 'WHO', 'WHY', 'WIG', 'WIN', 'WIZ', 'WOW', 'YAK', 'YAY', 'YES', 'ZAP', 'ZIG', 'ZOO', 'ZZZ',])
node_name_mapping = dict()
# keep as many names as possible the same
for tla in homophonic_node_names:
	if tla in new_node_names:
		node_name_mapping[tla] = tla
		new_node_names -= set([tla])
# and now assign the rest of the node names
new_node_names = sorted(new_node_names, reverse=True)
for tla in homophonic_node_names:
	if tla not in node_name_mapping.keys():
		node_name_mapping[tla] = new_node_names.pop()
assert(len(new_node_names)==0) # make sure all names were used

def extract_nodes(text):
	p = re.compile('([a-z]+)[\s\.]+(\d+)[\s\.]+([a-z]+)\s*\=\s*([a-z]+)[\s\.]+(\d+)[\s\.]+([a-z]+)')
	m = p.match(text)
	name1 = node_name_mapping[m.group(1).upper()]
	order1 = int(m.group(2))
	inout1 = m.group(3).upper()
	name2 = node_name_mapping[m.group(4).upper()]
	order2 = int(m.group(5))
	inout2 = m.group(6).upper()
	return name1, order1, inout1, name2, order2, inout2


def extract_step_number(text):
	p = re.compile('step\s+(\d+)\s+.*')
	m = p.match(text)
	step = m.group(1)
	return step


def fill_color(ax, color, alpha=1.):
	rect = mpatches.Rectangle([-0.3,-0.3],1.6,1.6, facecolor=color, alpha=alpha )#, ec="none")
	ax.add_patch(rect)
	ax.xaxis.set_ticks_position('none')
	ax.yaxis.set_ticks_position('none')
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])


def bar_location_diagram(ax, z, ii, color):
	shape = mpatches.Circle([0.5, 0.5], 0.4, fill=False, linewidth=8)
	# plt.setp(shape, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	ax.add_patch(shape)

	# print [z[0,ii], z[1,ii]]
	shape = mpatches.Circle([z[0,ii]*0.35+0.5, z[1,ii]*0.35+0.5], 0.15, fill=True, facecolor='black')
	plt.setp(shape, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	ax.add_patch(shape)
	plt.axis('off')


def make_node_label(ax, num, x, max_order):
	tla = x["node %d TLA"%(num)]

	# add a rectangle
	attr = node_attributes[tla]
	fill_color(ax, 'white')
	fill_color(ax, attr['color'], alpha=0.6)

	# add the text
	txt_core = tla
	txt = plt.text(0.35,0.5, txt_core, fontsize=fontsize_big, horizontalalignment='center',
         verticalalignment='center' ) #,  backgroundcolor='white', color='black')
	plt.setp(txt, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])


	node_order = x["node %d order"%(num)]
	# if this was an in node, make it an out node
	if x["node %d inout"%(num)] == 'IN':
		node_order = max_order[tla] - node_order + 1

	txt = plt.text(0.83,0.75, "%d"%node_order, fontsize=fontsize_small, horizontalalignment='center',
         verticalalignment='center' ) #,  backgroundcolor='white', color='black')
	plt.setp(txt, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	txt = plt.text(0.83,0.38, "-", fontsize=fontsize_small*2, horizontalalignment='center',
         verticalalignment='center' ) #,  backgroundcolor='white', color='black')
	plt.setp(txt, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	txt = plt.text(0.83,0.25, "%d"%max_order[tla], fontsize=fontsize_small, horizontalalignment='center',
         verticalalignment='center' ) #,  backgroundcolor='white', color='black')
	plt.setp(txt, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	plt.axis('off')

	return attr['color']


def single_bar_figure(X, z, ii, max_order):

	plt.figure(figsize=figsize)
	# break the sticker into 3 subplots

	# the size of the subplots
	gs = gridspec.GridSpec(1, 4, width_ratios=[1., 0.65, 0.6, 1.]) 


	# the left side subplot
	ax = plt.subplot(gs[0])
	color1 = make_node_label(ax, 1, X[ii], max_order)
	ax.axis([0,1, 0, 1])
	# the right side subplot
	ax = plt.subplot(gs[3])
	color2 = make_node_label(ax, 2, X[ii], max_order)
	ax.axis([0,1, 0, 1])
	
	# the sticker number subplot
	ax = plt.subplot(gs[1])
	fill_color(ax, 'white')
	fill_color(ax, color1, alpha=0.6)
	# fill_color(ax, center_color, alpha=0.7)
	txt = plt.text(0.5,0.5,X[ii]['step int'], fontsize=fontsize_big_num,horizontalalignment='center',
         verticalalignment='center')
	plt.setp(txt, path_effects=[PathEffects.withStroke(linewidth=3, foreground="w")])
	plt.axis('off')
	ax.axis([0,1, 0, 1])

	# the bar location subplot
	ax = plt.subplot(gs[2])
	fill_color(ax, 'white')
	fill_color(ax, color2, alpha=0.6)
	bar_location_diagram(ax, z, ii, color2)
	ax.axis([0,1, 0, 1])

	plt.subplots_adjust(left=-0.0001, bottom=-0.0001, right=1.0001, top=1.0001, wspace=-0.0001, hspace=-0.0001)

	fname = 'stickers/%d.pdf'%(X[ii]['step int'])
	plt.savefig(fname)
	plt.close()


def load_data(fname='Brain24ft_v0307-Jun-2014 091700_labels.csv'):

	# NOTE "nodes" is used to refer to both nodes and bars! TODO fix this naming convention

	X = np.genfromtxt(fname, delimiter=',', names=True, dtype=[('step', '|S50'), ('nodes', '|S50'), ('angles', '|S50'), ('length', '|S50')])
	X = recfunctions.append_fields(X, 'step int', np.zeros((X.shape[0],), dtype=int))
	X = recfunctions.append_fields(X, 'node 1 inout', np.zeros((X.shape[0],), dtype='|S3'))
	X = recfunctions.append_fields(X, 'node 2 inout', np.zeros((X.shape[0],), dtype='|S3'))
	X = recfunctions.append_fields(X, 'node 1 TLA', np.zeros((X.shape[0],), dtype='|S3'))
	X = recfunctions.append_fields(X, 'node 2 TLA', np.zeros((X.shape[0],), dtype='|S3'))
	X = recfunctions.append_fields(X, 'node 1 order', np.zeros((X.shape[0],), dtype=int))
	X = recfunctions.append_fields(X, 'node 2 order', np.zeros((X.shape[0],), dtype=int))
	for ii in range(X.shape[0]):
		X['step int'][ii] = extract_step_number(X['step'][ii])
		X['node 1 TLA'][ii], X['node 1 order'][ii], X['node 1 inout'][ii], \
		X['node 2 TLA'][ii], X['node 2 order'][ii], X['node 2 inout'][ii] = \
		extract_nodes(X['nodes'][ii])

	max_order = defaultdict(int)
	for ii in range(X.shape[0]):
		tla = X['node 1 TLA'][ii]
		order = X['node 1 order'][ii]
		if order > max_order[tla]:
			max_order[tla] = order
		tla = X['node 2 TLA'][ii]
		order = X['node 2 order'][ii]
		if order > max_order[tla]:
			max_order[tla] = order

	return X, max_order


def get_distances(X):
	# bar connectivity
	C = np.eye(X.shape[0])
	for ii in range(X.shape[0]):
		print "%d / %d"%(ii, X.shape[0])
		for jj in range(ii, X.shape[0]):
			if X['node 1 TLA'][ii] == X['node 1 TLA'][jj] or \
			   X['node 1 TLA'][ii] == X['node 2 TLA'][jj] or \
			   X['node 2 TLA'][ii] == X['node 1 TLA'][jj] or \
			   X['node 2 TLA'][ii] == X['node 2 TLA'][jj]:
				C[ii,jj] = 1
				C[jj,ii] = 1

	# bar distance
	D = np.ones((X.shape[0], X.shape[0]))*-1
	M = np.eye(X.shape[0])
	current_d = 0
	while np.min(D) < 0:
		D[(D<0) & (M>0)] = current_d
		current_d += 1
		M = np.dot(M, C)
		print current_d

	return D


def embed_bars(X, D):
	def f_df(z):
		z1 = z[:X.shape[0]]
		z2 = z[-X.shape[0]:]
		diff1 = z1.reshape((-1,1)) - z1.reshape((1,-1))
		diff2 = z2.reshape((-1,1)) - z2.reshape((1,-1))
		z_D = diff1**2 + diff2**2

		logdiff = np.log(z_D + np.eye(z_D.shape[0])) - np.log(D + np.eye(z_D.shape[0]))

		assert(np.sum(~np.isfinite(logdiff))==0)

		# DEBUG
		err = np.sum((z_D - D)**2 / (D+np.eye(D.shape[0]))**2)
		derrdz_D = 2.*(z_D - D) / (D + np.eye(z_D.shape[0]))**2
		# err = np.sum((z_D - D)**2 / (D+np.eye(D.shape[0])))
		# derrdz_D = 2.*(z_D - D) / (D + np.eye(z_D.shape[0]))
		# err = np.sum((z_D - D)**2)
		# derrdz_D = 2.*(z_D - D)
		# err = np.sum(logdiff**2)
		# derrdz_D = 2.*logdiff / (z_D + np.eye(z_D.shape[0]))
		# err = np.sum(logdiff**10)
		# derrdz_D = 10.*logdiff**9 / (z_D + np.eye(z_D.shape[0]))
		# err = np.sum(np.abs(logdiff))
		# derrdz_D = np.sign(logdiff) / (z_D + np.eye(z_D.shape[0]))

		derrddiff1 = derrdz_D*2.*diff1
		derrddiff2 = derrdz_D*2.*diff2
		derrdz1 = np.sum(derrddiff1, axis=1) - np.sum(derrddiff1, axis=0)
		derrdz2 = np.sum(derrddiff2, axis=1) - np.sum(derrddiff2, axis=0)

		derrdz = np.vstack((derrdz1.reshape((-1,1)), derrdz2.reshape((-1,1))))

		return err, derrdz.ravel()


	def fix_coords(X, z, node_nums, init=False):
		theta = np.linspace(0, 2.*np.pi, node_nums.shape[0]+1) + np.pi
		theta = theta[:-1]

		for ii in range(node_nums.shape[0]):
			match = np.flatnonzero(X['step int'] == node_nums[ii])
			assert(match.shape[0] == 1)
			if init:
				r = 100
			else:
				r = np.sqrt(np.sum(z[:,match]**2))
			z[0,match] = np.cos(theta[ii])*r
			z[1,match] = np.sin(theta[ii])*r
			if ii == 0:
				z[0,match] *= 0.8

	# these are the bars around the outside edge of the brain.
	fixed_node_nums = np.asarray([356, 357, 544, 653, 675, 669, 659, 631, 616, 617, 625, 635, 663, 647, 641, 567, 377])

	z = np.random.randn(2, X.shape[0])/100.
	fix_coords(X, z, fixed_node_nums, init=True)
	for i in range(100):
		z, _, _ = fmin_l_bfgs_b(
				f_df,
				z.ravel(),
				disp=1,
				maxfun=5)
		z = z.reshape((2,-1))
		fix_coords(X, z, fixed_node_nums)

	z, _, _ = fmin_l_bfgs_b(
			f_df,
			z.ravel(),
			disp=1,
			maxfun=2000)
	z = z.reshape((2,-1))

	z -= np.mean(z, axis=1).reshape((2,1))
	z /= np.max(z, axis=1).reshape((2,1))

	plt.figure()
	for ii in range(0, X.shape[0], 20):
		print "%d / %d"%(ii, X.shape[0])
		for jj in range(X.shape[0]):
			if D[ii,jj] == 1:
				plt.plot([z[0,ii], z[0,jj]], [z[1,ii], z[1,jj]], 'r')
	plt.plot(z[0,:], z[1,:], '.g')
	for ii in range(0, X.shape[0]):
		if X['step int'][ii] in fixed_node_nums:
			plt.plot(z[0,ii], z[1,ii], '*b')
		if X['step int'][ii] == fixed_node_nums[0]:
			plt.plot(z[0,ii], z[1,ii], '.y')

	return z


def max_order_histogram(max_order):
	"""
	How many nodes of each cardinality -- for ashley lighting node size email.
	"""
	histogram = defaultdict(int)
	for k in max_order.keys():
		histogram[max_order[k]] += 1
	print histogram


def main():
	print "loading data"
	X, max_order = load_data()
	print "(inefficiently) computing pairwise distances"
	D = get_distances(X)
	print "embedding bars in 2d space"
	z = embed_bars(X, D)

	print "node counts"
	max_order_histogram(max_order)

	target_bars = range(X.shape[0]) #[1,24,354,600,333,666,42]
	for ii in target_bars:
		single_bar_figure(X, z, ii, max_order)

if __name__ == '__main__':
	main()
