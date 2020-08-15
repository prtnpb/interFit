import time
import pandas as pd
import org_radwavefn

def j_qnum(k_quantum_num):
  if abs(k_quantum_num)==1:
    return('1/2')
  elif abs(k_quantum_num)==2:
    return('3/2')
  elif abs(k_quantum_num)==3:
    return('5/2')
  elif abs(k_quantum_num)==4:
    return('7/2')
  elif abs(k_quantum_num)==5:
    return('9/2')


def create_veusz_file(mode,atom):

  legend_labels_large=[]
  legend_labels_small=[]
  data_series_rad=[]
  data_series_lar=[]
  data_series_sma=[]
  page_names=[]

  # If we want to plot the results of a grasp2K calculation
  if mode=='plot_grasp_orbitals':
    with open(atom.element+'_grasp_numerical_orbitals.vsz','w') as g:
      for i in range(atom.orbital_info.num_orbitals):
        orb_text=atom.element+"_"+str(atom.orbital_info.n_qnums[i])+"_"+str(atom.orbital_info.k_qnums[i]).replace('-', 'n')

        page_names.append(orb_text)

        data_series_rad.append(orb_text+'_radialcomp')
        data_series_lar.append(orb_text+'_largecomp')
        data_series_sma.append(orb_text+'_smallcomp')

        legend_labels_large.append(str(atom.orbital_info.n_qnums[i])+str(org_radwavefn.ltolsym(org_radwavefn.lktol(atom.orbital_info.k_qnums[i])))+"("+str(j_qnum(atom.orbital_info.k_qnums[i]))+")")
        legend_labels_small.append(str(atom.orbital_info.n_qnums[i])+str(org_radwavefn.ltolsym(org_radwavefn.lktol(atom.orbital_info.k_qnums[i])))+'_small')

        g.write("ImportString(u'"+orb_text+"_radialcomp(numeric)','''\n")
        for rad_comp in atom.orbital_info.radial_comps[i]:
          g.write(str(rad_comp)+'\n')
        g.write("''')\n")
        g.write("ImportString(u'"+orb_text+"_largecomp(numeric)','''\n")
        for l_r in atom.orbital_info.large_div_r[i]:
          g.write(str(l_r)+'\n')
        g.write("''')\n")
        g.write("ImportString(u'"+orb_text+"_smallcomp(numeric)','''\n")
        for s_r in atom.orbital_info.small_div_r[i]:
          g.write(str(s_r)+'\n')
        g.write("''')\n")

      # Write out a page for each orbital
      g.write("Set('colorTheme', u'default-latest')\n")
      g.write("Set('StyleSheet/axis-function/autoRange', u'next-tick')\n")

      for page,large_legend,small_legend,data_rad,data_lar,data_sma in zip(page_names,legend_labels_large,legend_labels_small,data_series_rad,data_series_lar,data_series_sma):
        g.write("Add('page', name=u'"+page.replace('n','-')+"', autoadd=False)\n")
        g.write("To(u'"+page.replace('n','-')+"')\n")
        g.write("Add('graph', name=u'"+page.replace('n','-')+"', autoadd=False)\n")
        g.write("To(u'"+page.replace('n','-')+"')\n")
        g.write("Add('axis', name=u'x', autoadd=False)\n")
        g.write("To(u'x')\n")
        g.write("Set('label', u'r (angstroms)')\n")
        g.write("Set('min', u'Auto')\n")
        g.write("Set('max', u'Auto')\n")
        g.write("Set('Label/font', u'LMRoman10')\n")
        g.write("Set('TickLabels/font', u'LMRoman10')\n")
        g.write("To('..')\n")
        g.write("Add('axis', name=u'y', autoadd=False)\n")
        g.write("To(u'y')\n")
        g.write("Set('label', u'\\chi(r)/r')\n")
        g.write("Set('min', u'Auto')\n")
        g.write("Set('max', u'Auto')\n")
        g.write("Set('direction', u'vertical')\n")
        g.write("Set('Label/font', u'LMRoman10')\n")
        g.write("Set('TickLabels/font', u'LMRoman10')\n")
        g.write("To('..')\n")
        g.write("Add('xy', name=u'"+data_lar+"', autoadd=False)\n")
        g.write("To(u'"+data_lar+"')\n")
        g.write("Set('markerSize', u'1.5pt')\n")
        g.write("Set('xData', u'"+data_rad+"')\n")
        g.write("Set('yData', u'"+data_lar+"')\n")
        g.write("Set('key', u'"+large_legend+"')\n")
        g.write("To('..')\n")
        g.write("Add('xy', name=u'"+data_sma+"', autoadd=False)\n")
        g.write("To(u'"+data_sma+"')\n")
        g.write("Set('markerSize', u'1.5pt')\n")
        g.write("Set('xData', u'"+data_rad+"')\n")
        g.write("Set('yData', u'"+data_sma+"')\n")
        g.write("Set('key', u'"+small_legend+"')\n")
        g.write("Set('PlotLine/color', u'auto')\n")
        g.write("Set('MarkerLine/color', u'auto')\n")
        g.write("Set('MarkerFill/color', u'auto')\n")
        g.write("To('..')\n")
        g.write("Add('function', name=u'yax', autoadd=False)\n")
        g.write("To(u'yax')\n")
        g.write("Set('function', u'0')\n")
        g.write("Set('variable', u'y')\n")
        g.write("Set('Line/color', u'black')\n")
        g.write("To('..')\n")
        g.write("Add('function', name=u'xax', autoadd=False)\n")
        g.write("To(u'xax')\n")
        g.write("Set('function', u'0')\n")
        g.write("Set('Line/color', u'black')\n")
        g.write("To('..')\n")
        g.write("Add('key', name=u'key1', autoadd=False)\n")
        g.write("To(u'key1')\n")
        g.write("Set('title', u'')\n")
        g.write("Set('horzPosn', u'right')\n")
        g.write("Set('vertPosn', u'top')\n")
        g.write("Set('horzManual', 0.0)\n")
        g.write("Set('vertManual', 0.0)\n")
        g.write("To('..')\n")
        g.write("To('..')\n")
        g.write("To('..')\n")
 

  elif mode=='plot_orbital_equations':
    orbital=[]
    equation=[]

    with open('equations.dat') as g:
      for line in g:
        if '\n' in line:
          t=line.strip()
        else:
          t=line
        l=t.split()
        
        if len(l)==0:
          continue

        print(l)


        orbital.append(l[0])
        equation.append(l[1])


    with open(atom.element+'_orbital_equations_graph.vsz','w') as g:
      for orb,eqn in zip(orbital,equation):
        g.write("Add('page', name=u'"+orb+"', autoadd=False)\n")
        g.write("To(u'"+orb+"')\n")
        g.write("Add('graph', name=u'"+orb+"', autoadd=False)\n")
        g.write("To(u'"+orb+"')\n")
        g.write("Add('axis', name=u'x', autoadd=False)\n")
        g.write("To(u'x')\n")
        g.write("Set('label', u'r (angstroms)')\n")
        g.write("Set('min', u'Auto')\n")
        g.write("Set('max', u'Auto')\n")
        g.write("Set('Label/font', u'LMRoman10')\n")
        g.write("Set('TickLabels/font', u'LMRoman10')\n")
        g.write("To('..')\n")
        g.write("Add('axis', name=u'y', autoadd=False)\n")
        g.write("To(u'y')\n")
        g.write("Set('label', u'\\chi(r)/r')\n")
        g.write("Set('min', u'Auto')\n")
        g.write("Set('max', u'Auto')\n")
        g.write("Set('direction', u'vertical')\n")
        g.write("Set('Label/font', u'LMRoman10')\n")
        g.write("Set('TickLabels/font', u'LMRoman10')\n")
        g.write("To('..')\n")

        g.write("Add('function', name=u'"+orb+"', autoadd=False)\n")
        g.write("To(u'"+orb+"')\n")
        g.write("Set('function', u'"+eqn+"')\n")
        g.write("Set('key', u'"+orb+"')\n")
        g.write("Set('steps',10000)\n") 
        g.write("Set('Line/color', u'black')\n")
        g.write("To('..')\n")

        g.write("Add('function', name=u'yax', autoadd=False)\n")
        g.write("To(u'yax')\n")
        g.write("Set('function', u'0')\n")
        g.write("Set('variable', u'y')\n")
        g.write("Set('Line/color', u'black')\n")
        g.write("To('..')\n")

        g.write("Add('function', name=u'xax', autoadd=False)\n")
        g.write("To(u'xax')\n")
        g.write("Set('function', u'0')\n")
        g.write("Set('Line/color', u'black')\n")
        g.write("To('..')\n")
        g.write("Add('key', name=u'key1', autoadd=False)\n")
        g.write("To(u'key1')\n")
        g.write("Set('title', u'')\n")
        g.write("Set('horzPosn', u'right')\n")
        g.write("Set('vertPosn', u'top')\n")
        g.write("Set('horzManual', 0.0)\n")
        g.write("Set('vertManual', 0.0)\n")
        g.write("To('..')\n") 
        g.write("To('..')\n")
        g.write("To('..')\n") 


if __name__=='__main__':
  print('Running Module File')

  element=org_radwavefn.atomic_system('isodata','rwfn.out')

  create_veusz_file('plot_grasp_orbitals', element)
  create_veusz_file('plot_orbital_equations', element)

