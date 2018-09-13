import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud

def plot_email_header_stat(email_header_stat, nstat):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	width = 0.35
	positive_x = np.arange(nstat)
	negative_x = positive_x + width

	positive_y = []
	negative_y = []
	x_tick_marks = []
	for field in email_header_stat['positive']: 
		x_tick_marks.append(field)
		positive_y.append(email_header_stat['positive'][field])
		negative_y.append(email_header_stat['negative'][field])

	positive_bar = ax.bar(positive_x, positive_y, width, color='blue')
	negative_bar = ax.bar(negative_x, negative_y, width, color='red')

	# axes limit
	ax.set_xlim(-width, len(positive_x)+width)
	ax.set_ylim(0, max(positive_y+negative_y)+20)
	# y label and figure title
	ax.set_ylabel('Freq')
	ax.set_title('email header features compare')
	# x ticks
	ax.set_xticks(negative_x)
	tick_names = ax.set_xticklabels(x_tick_marks)
	plt.setp(tick_names, rotation=45, fontsize=10)
	## add legend
	ax.legend((positive_bar[0], negative_bar[0]), ('Positive', 'Negative'))

	plt.show()


def plot_email_body_stat(email_body_stat, plot_wordcloud=True, plot_wordhist=True):
	if plot_wordcloud:
		positive_wc = WordCloud().generate(email_body_stat['positive']['__body__'])
		negative_wc = WordCloud().generate(email_body_stat['negative']['__body__'])
		plt.figure('positive wordcloud')
		plt.imshow(positive_wc, interpolation='bilinear')
		plt.axis('off')
		plt.figure('negative wordcloud')
		plt.imshow(negative_wc, interpolation='bilinear')
		plt.axis('off')

	if plot_wordhist:
		inner_tokens = set(['__body__'])
		nbins = 50
		token_id_dict = email_body_stat['tokens']
		fig = plt.figure('word scatter')
		ax = fig.add_subplot(121)
		positive_x = [token_id_dict.get(token, 0) for token in email_body_stat['positive'] if token not in inner_tokens]
		negative_x = [token_id_dict.get(token, 0) for token in email_body_stat['negative'] if token not in inner_tokens]
		ax.hist(positive_x, nbins, color='black')
		ax.hist(negative_x, nbins, color='red')

	plt.show()

def plot_cross_validation(precision_list, recall_list):
	fig = plt.figure('precision & recall')
	ax = fig.add_subplot(131)
	precision_list = [i*100 for i in precision_list]
	recall_list = [i*100 for i in recall_list]
	
	ax.scatter(precision_list, recall_list, color='blue')
	# ax.set_aspect(1./ax.get_data_ratio())
	# ax.plot(precision_list, recall_list)
	ax.set_xlabel('Precision')
	ax.set_ylabel('Recall')

	avg_precision = int(sum(precision_list) / len(precision_list))
	avg_recall = int(sum(recall_list) / len(recall_list))
	plt.plot([avg_precision, avg_precision], [min(recall_list), max(recall_list)], 'k-', linewidth=2)
	plt.plot([min(precision_list), max(precision_list)], [avg_recall, avg_recall], 'k-', linewidth=2)

	plt.grid(True)
	plt.show()