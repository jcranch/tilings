import matplotlib.pyplot as plt

def line_plot_2d(list_of_dictionary_of_y_s, x_s = False, 
                number_of_rows = 1,number_of_columns = 1,position_code = 1,
                figure = False,
                legend_on = True, marker_style = 'polygon',
                x_label = 'Iteration', y_label = 'Polygon Count',index_start = False , index_end = False, 
                save_on = True, save_name = 'data_lines_image',folder = 'demos/datalines'):
    
    '''
    This is a function for plotting multiple data lines on one 2d graph.
    
    list_of_dictionary_of_ys should be of the form
    [...{'name':'data_name', 'data':y_s, 'colour' : data_colour, 'alpha' : 1 }...]. 
    
    It is recommended to use the polygon_count functions to help create this.
    
    If marker_style = 'polygon' an 'n-gon' will be used as the marker. 
    
    Number of rows and number of columns determines how the figure is subdivided into equal areas
    and the position code decides which area the subplot is plotted in. 
    
    To plot in the area in the i^{th} row and j^{th} the position code should be 
    j + (i-1)*j . 
    
    For example to plot in the top right quarter of a pictre we use 
    number_of_rows = 2, number_of_columns = 2, position_code = 1.
    '''

    if figure == False:
        figure = plt.figure(figsize(20,5))
    if x_s == False:
        maxx = len(list_of_dictionary_of_y_s[0]['data'])+1
        x_s = range(1,maxx)
        
    if index_start:
        x_s = x_s[index_start:]
        for dictionary_of_y_s in list_of_dictionary_of_y_s:
            dictionary_of_y_s['data'] = dictionary_of_y_s['data'][index_start:]
            
    if index_end:
        x_s = x_s[:index_end]
        for dictionary_of_y_s in list_of_dictionary_of_y_s:
            dictionary_of_y_s['data'] = dictionary_of_y_s['data'][:index_end] 
            
    max_value = 0.0
    for dictionary_of_y_s in list_of_dictionary_of_y_s:
        max_data = max(dictionary_of_y_s['data'])
        if  max_data > max_value:
            max_value = max_data 
             
    axis = plt.subplot(number_of_rows,number_of_columns ,position_code, frameon = False,
                                     xlim = (-1.01+index_start, maxx*1.1), 
                                     ylim = (-0.01, max_value*1.1 ))
    axis.set_xlabel(x_label, fontsize = 18)
    axis.set_ylabel(y_label, fontsize = 18)
    axis.grid(True)
    lines = []
    marker_frequency = (len(x_s)-1,len(x_s)-1)
    if len(x_s) == 1:
        marker_frequency = 1
    marker_style_ = marker_style
    for dictionary_of_y_s in list_of_dictionary_of_y_s:
        if marker_style == 'polygon':
            marker_style_ = (dictionary_of_y_s['n'],0,0)
        lines.append(axis.plot(x_s,dictionary_of_y_s['data'],linestyle = '-', label = dictionary_of_y_s['name'],
                               color = dictionary_of_y_s['colour'],alpha = dictionary_of_y_s['alpha'], 
                               marker = marker_style_, markersize = 10,
                               markevery = marker_frequency, markeredgecolor = dictionary_of_y_s['colour'])[0])
        
    if legend_on == True:
        axis.legend(loc = 'upper right',framealpha = 0.0, fancybox = True)
    if save_on:
        folder_name = os.path.join(folder)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name) 
        figure.savefig(folder+'/'+str(save_name)+'.png')  
    return axis
