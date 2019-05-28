# ------------------------------------------------------------------------
# Plota_Versao_2_SERIE_PSD_DFA.pyplot
# ------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import stats, optimize
import numpy as np
import math
from powernoise import powernoise
from logistic import logistic
from pmodel import pmodel
import preprocess as pre

__author__ = 'Paulo Giovani'
__copyright__ = 'Copyright 2017, 3DBMO Project INPE'
__credits__ = ['Paulo Giovani', 'Reinaldo Roberto Rosa', 'Murilo da Silva Dantas']
__license__ = 'GPL'
__version__ = '0.1B'
__maintainer__ = 'Paulo Giovani'
__email__ = 'pg_faria@yahoo.com.br'

#---------------------------------------------------------------------
# Calcula o PSD da serie temporal
#---------------------------------------------------------------------
def psd(data):
	"""Calcula o PSD de uma serie temporal."""
	
	# Define um intervalo para realizar o ajuste da reta
	INICIO = 10
	FIM = 250
	
	# O vetor com o tempo e o tamanho do numero de pontos
	N = len(data)
	tempo = np.arange(len(data))

	# Define a frequencia de amostragem
	dt = (tempo[-1] - tempo[0] / (N - 1))
	fs = 1 / dt

	# Calcula o PSD utilizando o MLAB
	power, freqs = mlab.psd(data, Fs = fs, NFFT = N, scale_by_freq = False)

	# Calcula a porcentagem de pontos utilizados na reta de ajuste
	totalFrequencias = len(freqs)
	totalPSD = FIM - INICIO
	porcentagemPSD = int(100 * totalPSD / totalFrequencias)

	# Seleciona os dados dentro do intervalo de selecao
	xdata = freqs[INICIO:FIM]
	ydata = power[INICIO:FIM]

	# Simula o erro
	yerr = 0.2 * ydata

	# Define uma funcao para calcular a Lei de Potencia
	powerlaw = lambda x, amp, index: amp * (x**index)

	# Converte os dados para o formato LOG
	logx = np.log10(xdata)
	logy = np.log10(ydata)

	# Define a funcao para realizar o ajuste
	fitfunc = lambda p, x: p[0] + p[1] * x
	errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err    
	logyerr = yerr / ydata

	# Calcula a reta de ajuste
	pinit = np.asarray([1.0, -1.0])
	out = optimize.leastsq(errfunc, pinit, args = (logx, logy, logyerr), full_output = True)
	pfinal = out[0]
	covar = out[1]
	index = pfinal[1]
	amp = 10.0 ** pfinal[0]
	indexErr = np.sqrt(covar[0][0])
	ampErr = np.sqrt(covar[1][1]) * amp
	
	# Retorna os valores obtidos
	return freqs, power, xdata, ydata, amp, index, powerlaw, INICIO, FIM
	
#---------------------------------------------------------------------
# Calcula o DFA 1D da serie temporal
#---------------------------------------------------------------------
def dfa1d(timeSeries, grau):
	"""Calcula o DFA 1D (adaptado de Physionet), onde a escala cresce
	de acordo com a variavel 'Boxratio'. Retorna o array 'vetoutput',
	onde a primeira coluna e o log da escala S e a segunda coluna e o
	log da funcao de flutuacao."""

	# 1. A serie temporal {Xk} com k = 1,..., N e integrada na chamada funcao perfil Y(k)
	x = np.mean(timeSeries)
	timeSeries = timeSeries - x
	yk = np.cumsum(timeSeries)
	tam = len(timeSeries)

	# 2. A serie (ou perfil) Y(k) e dividida em N intervalos nao sobrepostos de tamanho S
	sf = np.ceil(tam / 4).astype(np.int)
	boxratio = np.power(2.0, 1.0 / 8.0)
	vetoutput = np.zeros(shape = (1,2))

	s = 4
	while s <= sf:        
		serie = yk        
		if np.mod(tam, s) != 0:
			l = s * int(np.trunc(tam/s))
			serie = yk[0:l]			
		t = np.arange(s, len(serie), s)
		v = np.array(np.array_split(serie, t))
		l = len(v)
		x = np.arange(1, s + 1)
		
		# 3. Calcula-se a variancia para cada segmento v = 1,...,n_s:
		p = np.polynomial.polynomial.polyfit(x, v.T, grau)
		yfit = np.polynomial.polynomial.polyval(x, p)
		vetvar = np.var(v - yfit)
		
		# 4. Calcula-se a funcao de flutuacao DFA como a media das variancias de cada intervalo
		fs = np.sqrt(np.mean(vetvar))
		vetoutput = np.vstack((vetoutput,[s, fs]))
		
		# A escala S cresce numa serie geometrica
		s = np.ceil(s * boxratio).astype(np.int)

	# Array com o log da escala S e o log da funcao de flutuacao
	vetoutput = np.log10(vetoutput[1::1,:])

	# Separa as colunas do vetor 'vetoutput'
	x = vetoutput[:,0]
	y = vetoutput[:,1]

	# Regressao linear
	slope, intercept, _, _, _ = stats.linregress(x, y)

	# Calcula a reta de inclinacao
	predict_y = intercept + slope * x

	# Calcula o erro
	pred_error = y - predict_y

	# Retorna o valor do ALFA, o vetor 'vetoutput', os vetores X e Y,
	# o vetor com os valores da reta de inclinacao e o vetor de erros
	return slope, vetoutput, x, y, predict_y, pred_error

#---------------------------------------------------------------------
# Trecho principal
#---------------------------------------------------------------------
def main():
	"""Funcao com o codigo principal do programa."""
	
	print("\nData Analysis for 3DBMO simulations...\n")
	
	# Desabilita as mensagens de erro do Numpy (warnings)
	old_settings = np.seterr(divide = 'ignore', invalid = 'ignore', over = 'ignore')
	
	# Carrega o arquivo de dados
	nomeArquivo = 'surftemp504.txt'
	data = np.genfromtxt(nomeArquivo, dtype = 'float32', filling_values = 0)

	# Numero de amostras do sinal
	n_samples = 1024

	# Ruido vermelho
	S3 = powernoise(2, n_samples)

	# Caos, usado para gerar o sinal S7
	rho = 3.85
	a0 = 0.001
	S4 = logistic(rho, a0, n_samples)

	# Soma os sinais e normalizae modo que <A>=0 e std=1
	S7 = pre.standardize(S3 + S4)

	# Sinal gerado pelo pmodel
	S8 = pmodel(noValues=n_samples, p=0.52, slope=-1.66)

	# data = S8

	# Exibe os primeiro N valores do arquivo
	N = 10
	print("Original time series data (%d points): \n" %(len(data)))
	print("First %d points: %s\n" %(N, data[0:10]))
	print()
	
	#-----------------------------------------------------------------
    # Parametros gerais de plotagem
    #-----------------------------------------------------------------
	
	# Define os subplots
	fig = plt.figure()
	fig.subplots_adjust(hspace = .3, wspace = .2)
	
	# Tamanho das fontes
	tamanhoFonteEixoX = 16
	tamanhoFonteEixoY = 16
	tamanhoFonteTitulo = 16
	tamanhoFontePrincipal = 25
	
	# Titulo principal
	tituloPrincipal = '3DBMO Time Series Analysis' 	
	
	#-----------------------------------------------------------------
    # Plotagem da serie original
    #-----------------------------------------------------------------
	
	# Define as cores da plotagem
	corSerieOriginal = 'r'
	
	# Titulo dos eixos da serie original
	textoEixoX = 'Tempo'
	textoEixoY = 'Amplitude'
	textoTituloOriginal = 'Original Time Series Data'
	
	print("1. Plotting time series data...")
	
	# Plotagem da serie de dados    
	#O = fig.add_subplot(1, 3, 1)    
	O = fig.add_subplot(2, 1, 1)
	O.plot(data, '-', color = corSerieOriginal)
	O.set_title(textoTituloOriginal, fontsize = tamanhoFonteTitulo)
	O.set_xlabel(textoEixoX, fontsize = tamanhoFonteEixoX)
	O.set_ylabel(textoEixoY, fontsize = tamanhoFonteEixoY)
	O.ticklabel_format(style = 'sci', axis = 'x', scilimits = (0,0))
	O.grid()
	
	#-----------------------------------------------------------------
    # Calculo e plotagem do PSD
    #-----------------------------------------------------------------
	
	# Calcula o PSD
	freqs, power, xdata, ydata, amp, index, powerlaw, INICIO, FIM = psd(data)

	# O valor do beta equivale ao index
	b = index

	# Define as cores da plotagem
	corPSD1 = 'k'
	corPSD2 = 'navy'

	# Titulo dos eixos do PSD
	textoPSDX = 'Frequencia (Hz)'
	textoPSDY = 'Potencia'
	textoTituloPSD = r'Power Spectrum Density $\beta$ = '
	
	print("2. Plotting Power Spectrum Density...")

	# Plotagem do PSD    
	PSD = fig.add_subplot(2, 2, 3)    
	PSD.plot(freqs, power, '-', color = corPSD1, alpha = 0.7)
	PSD.plot(xdata, ydata, color = corPSD2, alpha = 0.8)
	PSD.axvline(freqs[INICIO], color = corPSD2, linestyle = '--')
	PSD.axvline(freqs[FIM], color = corPSD2, linestyle = '--')    
	PSD.plot(xdata, powerlaw(xdata, amp, index), 'r-', linewidth = 1.5, label = '$%.4f$' %(b))    
	PSD.set_xlabel(textoPSDX, fontsize = tamanhoFonteEixoX)
	PSD.set_ylabel(textoPSDY, fontsize = tamanhoFonteEixoY)
	PSD.set_title(textoTituloPSD + '%.4f' %(b), loc = 'center', fontsize = tamanhoFonteTitulo)
	PSD.set_yscale('log')
	PSD.set_xscale('log')
	PSD.grid() 
	
	#-----------------------------------------------------------------
	# Calculo e plotagem do DFA
    #-----------------------------------------------------------------
	        
	# Calcula o DFA 1D
	alfa, vetoutput, x, y, reta, erro = dfa1d(data, 1)

	# Verifica se o DFA possui um valor valido
	# Em caso afirmativo, faz a plotagem
	if not math.isnan(alfa):
		
		# Define as cores da plotagem
		corDFA = 'darkmagenta'

		# Titulo dos eixos do DFA
		textoDFAX = '$log_{10}$ (s)'
		textoDFAY = '$log_{10}$ F(s)'
		textoTituloDFA = r'Detrended Fluctuation Analysis $\alpha$ = '
		
		print("3. Plotting Detrended Fluctuation Analysis...")
		
		# Plotagem do DFA 
		DFA = fig.add_subplot(2, 2, 4)    
		DFA.plot(x, y, 's', 
				 color = corDFA, 
				 markersize = 4,
				 markeredgecolor = 'r',
				 markerfacecolor = 'None',
				 alpha = 0.8)				 
		DFA.plot(x, reta, '-', color = corDFA, linewidth = 1.5)
		DFA.set_title(textoTituloDFA + '%.4f' %(alfa), loc = 'center', fontsize = tamanhoFonteTitulo)
		DFA.set_xlabel(textoDFAX, fontsize = tamanhoFonteEixoX)
		DFA.set_ylabel(textoDFAY, fontsize = tamanhoFonteEixoY)
		DFA.grid()

	else:  
		DFA = fig.add_subplot(2, 2, 4)
		DFA.set_title(textoTituloDFA + 'N.A.', loc = 'center', fontsize = tamanhoFonteTitulo)
		DFA.grid()

	#-----------------------------------------------------------------
	# Exibe e salva a figura
	#-----------------------------------------------------------------
	plt.suptitle(tituloPrincipal, fontsize = tamanhoFontePrincipal)
	nomeImagem = '3DBMO_PSD_DFA_2.png'
	fig.set_size_inches(15, 9)
	plt.savefig(nomeImagem, dpi = 300, bbox_inches = 'tight', pad_inches = 0.1)	
	plt.show()
    
#---------------------------------------------------------------------
# Trecho principal
#---------------------------------------------------------------------
if __name__ == "__main__":
	main()
