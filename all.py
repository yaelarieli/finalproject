def fit_linear(filename):
    file=open(filename)
    datafile=file.readlines()

    #get lists for x,dx,y,dx,x axis,y axis.
    def get_x_and_y_lists(temp_file):
        data_befor_lower=[]
        x_axis = None
        y_axis = None
        for line in temp_file:
            #line_lower = line.lower()
            linesplit = line.strip().split(' ')
            if 'axis:' in linesplit and 'x' in linesplit:
                x_axis = (linesplit[2:])
            elif 'y' in linesplit and 'axis:' in linesplit:
                y_axis = (linesplit[2:])
            else:
                data_befor_lower.append(linesplit)
        data_befor_lower.remove([''])
        data = []
        for a_list in data_befor_lower:
            temp_list=[]
            for item in a_list:
                lower_letter=item.lower()
                temp_list.append(lower_letter)
            try:
                temp_list.remove('')
                data.append(temp_list)
            except:
                data.append(temp_list)

        tables = ['x', 'dx', 'y', 'dy']
        data_list = []
        #colons
        if data[0][0] in tables and data[0][1] in tables:
            for i in tables:
                z=[]
                if i in data[0]:
                    place=data[0].index(i)
                    for row in range(1,len(data)):
                        try:
                            z.append(float(data[row][place]))
                        except:
                            continue
                data_list.append(z)
        #rows
        else:
            for i in tables:
                z = []
                string_list=None
                for line in data:
                    if i in line:
                        string_list=(line[1:len(line)+1])
                        for number in string_list:
                            z.append(float(number))
                data_list.append(z)
        x_y_values=[]
        x_y_values.append(data_list)
        x_y_values.append(x_axis)
        x_y_values.append(y_axis)
        return(x_y_values)

    #find if there are any error in the data.
    def find_errors(xData, dxData, yData, dyData):
        # xData,dxData,yData,dyData=get_x_and_y_lists(datafile)
        if 0 in dxData or 0 in dyData:
            print('Input file error: Not all uncertainties are positive.')
            return
        elif len(xData) != len(dxData) or len(yData) != len(dyData) or len(yData) != len(xData):
            print('Input file error: Data lists are not the same length.')
            return
        else:
            for item in dxData:
                if item < 0:
                    print('Input file error: Not all uncertainties are positive.')
                    return
            for item in dyData:
                if item < 0:
                    print('Input file error: Not all uncertainties are positive.')
                    return
        return (xData, dxData, yData, dyData)

    #get the averages data
    def get_averages(x, y, dy):
        before_sigma_one_divid_dy_squared = []
        dy_squared = []
        for num in dy:
            squard = num ** 2
            dy_squared.append(squard)
            before_sigma_one_divid_dy_squared.append(1 / squard)
        sigma_one_divid_dy_squared = sum(before_sigma_one_divid_dy_squared)

        x_squared = []
        for num in x:
            squ = num ** 2
            x_squared.append(squ)
        xy = []
        i = 0
        while i < len(y):
            for x_i in x:
                xi_double_yi = x_i * y[i]
                i = i + 1
                xy.append(xi_double_yi)

        before_sum = []
        get_av = [x, y, dy_squared, x_squared, xy]
        for list in get_av:
            sub_list = []
            dy_i_sum = 0
            while dy_i_sum < len(dy_squared):
                for i in list:
                    up = i / dy_squared[dy_i_sum]
                    sub_list.append(up)
                    dy_i_sum = dy_i_sum + 1
            before_sum.append(sub_list)
        x_average = (sum(before_sum[0])) / sigma_one_divid_dy_squared
        y_average = (sum(before_sum[1])) / sigma_one_divid_dy_squared
        dy_squr_avg = (sum(before_sum[2])) / sigma_one_divid_dy_squared
        x_squared_avg = (sum(before_sum[3])) / sigma_one_divid_dy_squared
        xy_avg = (sum(before_sum[4])) / sigma_one_divid_dy_squared
        N = len(x)
        return (x_average, y_average, dy_squr_avg, x_squared_avg, xy_avg,N)


    #get a , da, b,db
    def find_a_and_b(x_average, y_average, dy_squr_avg, x_squared_avg, xy_avg, N):
        a = (xy_avg - (x_average * y_average)) / (x_squared_avg - (x_average ** 2))
        b = y_average - (a * x_average)
        da = (dy_squr_avg / (N * (x_squared_avg - (x_average ** 2)))) ** 0.5
        db = ((dy_squr_avg * x_squared_avg) / (N * (x_squared_avg - (x_average ** 2)))) ** 0.5
        return (a, da, b, db)

    #get chi red
    def find_chi(a, b, xData, yData, dyData, N):
        before_sum_chi_squr = []
        i = 0
        for x_i in xData:
            minimaze_chi = ((yData[i] - ((a * x_i) + b)) / dyData[i]) ** 2
            before_sum_chi_squr.append(minimaze_chi)
            i = i + 1
        chi_squared = sum(before_sum_chi_squr)
        chi_squared_red = chi_squared / (N - 2)
        return (chi_squared,chi_squared_red)


    #axis names
    def axis_names(x_axis_list,y_axis_list):
        x_axis_before = ''
        for i in range(0, len(x_axis_list)):
            x_axis_before = x_axis_before + ' ' + x_axis_list[i]
        x_axis = x_axis_before.strip()
        y_axis_before = ''
        for i in range(0, len(y_axis_list)):
            y_axis_before = y_axis_before + " " + y_axis_list[i]
        y_axis = y_axis_before.strip()
        return(x_axis,y_axis)

    #find new list of y for the fit line.
    def find_y_of_fit(xData, a, b):
        new_y = []
        for x_i in xData:
            y = (x_i * a) + b
            new_y.append(y)
        return new_y

    temp_file = get_x_and_y_lists(datafile)
    xData, dxData, yData, dyData = find_errors(temp_file[0][0], temp_file[0][1], temp_file[0][2], temp_file[0][3])
    x_y_values=get_x_and_y_lists(datafile)
    x_axis_list,y_axis_list=x_y_values[1],x_y_values[2]
    x_axis,y_axis=axis_names(x_axis_list,y_axis_list)
    x_average, y_average, dy_squr_avg, x_squared_avg, xy_avg, N = get_averages(xData, yData, dyData)
    a, da, b, db = find_a_and_b(x_average, y_average, dy_squr_avg, x_squared_avg, xy_avg, N)
    chi_squared,chi_squared_red=find_chi(a, b, xData, yData, dyData, N)
    new_y=find_y_of_fit(xData,a,b)

    import matplotlib.pyplot as plt

    plt.plot(xData,new_y,color='red')
    plt.errorbar(xData,yData,xerr=dxData,yerr=dyData,ecolor='blue',fmt='None')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.show()
    plt.savefig("linear_fit.SVG")
    print('a =',a,'+-',da,'\nb =',b,'+-',db,'\nchi2 =',chi_squared,'\nchi2_reduced =',chi_squared_red)
    return

print(fit_linear('file'))
