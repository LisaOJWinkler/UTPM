"""Module containing main method for the UTPM"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import matplotlib.pylab as pl
import seaborn as sns

import sub_models
import evolve_fleet123

print("This is my file to test Python's execution methods.")
print("The variable __name__ tells me which context this file is running in.")
print("The value of __name__ is:", repr(__name__))

def Run_Model(phase_out_date,phase_out_hybrid,scrap_age_pre2020,scrap_age_post2020,mass,fleet_size_projection,miles_driven_projection,retrofit_percentage,manufacture,elec,rate):
      """
      UTPM main method
      """

      #Print policy choices
      print('Policies: Phase-Out:',phase_out_date,'Hybrid Phase-Out:',phase_out_hybrid,'Scrap Age:',scrap_age_post2020,\
            'Light-weighting:',mass,'Modal shift:',fleet_size_projection,'Retro-fitting:',retrofit_percentage,\
            'Regulated manufacture:',manufacture,'Electricity decarb:',elec,'Modal Shift Rate:',rate)

      print("Running model...")

      #Run evolve fleet function with parameters given
      
      total,bev,petrol,diesel,hybrid,conv,ages,electric_emissions,tailpipe_emissions,mod_shift_emiss,elec_demand,foss_demand,\
      mod_shift_energy,ev_prod_emissions,ice_prod_emissions,conv_prod_emissions,ev_prod_energy,ice_prod_energy,conv_prod_energy,\
      km_driven=evolve_fleet123.evolve_fleet(phase_out_date,phase_out_hybrid,scrap_age_pre2020,scrap_age_post2020,mass,\
                  fleet_size_projection,miles_driven_projection,retrofit_percentage,manufacture,elec,rate)
      
      if __name__ == '__main__':

            #Make emission graphs for the model run
            SMALL_SIZE = 15
            MEDIUM_SIZE = 17
            BIGGER_SIZE = 18
            plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
            plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
            plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
            plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
            plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
            plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
            
            fig, axs = plt.subplots(1, 3,figsize=(16,6))
            # horizontal space between axes
            fig.subplots_adjust(wspace=0.5)

            axs[0].set_ylabel("Number of Cars in\n London (thousands)")
            axs[0].set_xlabel("Year")
            axs[0].plot(range(2020,2051),total,label='Total cars')
            axs[0].plot(range(2020,2051),bev,label='BEV cars')
            axs[0].plot(range(2020,2051),petrol,label='Petrol cars')
            axs[0].plot(range(2020,2051),diesel,label='Diesel cars')
            axs[0].plot(range(2020,2051),conv,label='Retrofitted cars')
            axs[0].plot(range(2020,2051),hybrid,label='PHEV cars')
            axs[0].legend(bbox_to_anchor=(0.8,-0.2))
            axs[0].set_xlim(2020,2050)
            axs[0].grid()

            axs[1].stackplot(range(2020,2051),np.array(electric_emissions)/10**12,np.array(tailpipe_emissions)/10**12,np.array(ev_prod_emissions)/10**9,np.array(ice_prod_emissions)/10**9,np.array(conv_prod_emissions)/10**9,np.array(mod_shift_emiss), labels=['Electricity Emissions','Tailpipe Emissions','EV Embedded Emissions','ICE Embedded Emissions','Retrofit Embedded Emissions','Replacement Mode Emissions'],colors=['black','blue','red','orange','purple','skyblue'],alpha=0.8,linestyle='None')
            axs[1].set_ylabel('Emissions (MtCO2)')
            axs[1].set_xlabel('Year')
            #axs[1].legend(bbox_to_anchor=(1.7, 0.7))
            axs[1].set_xlim(2020,2050)
            axs[1].grid()

            axs[2].stackplot(range(2020,2051),np.cumsum(np.array(electric_emissions)/10**12),np.cumsum(np.array(tailpipe_emissions)/10**12),np.cumsum(np.array(ev_prod_emissions)/10**9),np.cumsum(np.array(ice_prod_emissions)/10**9),np.cumsum(np.array(conv_prod_emissions)/10**9),np.cumsum(np.array(mod_shift_emiss)), labels=['Electricity Emissions','Tailpipe Emissions','EV Embedded Emissions','ICE Embedded Emissions','Retrofit Embedded Emissions','Replacement Mode Emissions'],colors=['black','blue','red','orange','purple','skyblue'],alpha=0.8,linestyle='None')
            axs[2].set_ylabel('Cumulative Emissions (MtCO2)')
            axs[2].set_xlabel('Year')
            axs[2].legend(bbox_to_anchor=(0.3,-0.2))
            axs[2].set_xlim(2020,2050)
            axs[2].grid()

            plt.show()

            #Make energy demand graphs
            plt.figure()
            plt.stackplot(range(2020,2051),np.array(elec_demand),np.array(foss_demand),np.array(ev_prod_energy),np.array(ice_prod_energy),np.array(conv_prod_energy),np.array(mod_shift_energy), labels=['Electricity','Fossil Fuel Energy','EV Embedded Energy','ICE Embedded Energy','Retrofit Embedded Energy','Replacement Mode Energy'],colors=['black','blue','red','orange','purple','skyblue'],alpha=0.8,linestyle='None')
            plt.ylabel('Energy Demand (MJ)')
            plt.xlabel('Year')
            plt.legend(bbox_to_anchor=(1.9, 0.7))
            plt.xlim(2020,2050)
            plt.grid()
            plt.show()

            plt.figure()
            plt.stackplot(range(2020,2051),np.cumsum(np.array(elec_demand)),np.cumsum(np.array(foss_demand)),np.cumsum(np.array(ev_prod_energy)),np.cumsum(np.array(ice_prod_energy)),np.cumsum(np.array(conv_prod_energy)),np.cumsum(np.array(mod_shift_energy)), labels=['Electricity','Fossil Fuel Energy','EV Embedded Energy','ICE Embedded Energy','Retrofit Embedded Energy','Replacement Mode Energy'],colors=['black','blue','red','orange','purple','skyblue'],alpha=0.8,linestyle='None')
            plt.ylabel('Cumulative\nEnergy Demand (MJ)')
            plt.xlabel('Year')
            plt.legend(bbox_to_anchor=(1.9, 0.7))
            plt.xlim(2020,2050)
            plt.grid()
            plt.show()


      cum_electric=np.append(0,np.cumsum(np.array(electric_emissions)/10**12))
      cum_tailpipe=np.append(0,np.cumsum(np.array(tailpipe_emissions)/10**12))
      cum_ev_prod=np.append(0,np.cumsum(np.array(ev_prod_emissions)/10**9))
      cum_ice_prod=np.append(0,np.cumsum(np.array(ice_prod_emissions)/10**9))
      cum_conv_prod=np.append(0,np.cumsum(np.array(conv_prod_emissions)/10**9))
      cum_mod_shift_emiss=np.append(0,np.cumsum(np.array(mod_shift_emiss)))

      cum_elec=np.append(0,np.cumsum(np.array(elec_demand)))
      cum_foss=np.append(0,np.cumsum(np.array(foss_demand)))
      cum_ev_en=np.append(0,np.cumsum(np.array(ev_prod_energy)))
      cum_ice_en=np.append(0,np.cumsum(np.array(ice_prod_energy)))
      cum_conv_en=np.append(0,np.cumsum(np.array(conv_prod_energy)))
      cum_mod_en=np.append(0,np.cumsum(np.array(mod_shift_energy)))
      
      #returns emissions by type, cumulative emissions by type, energy demand by type, cumulative energy demand by type,
      #age of fleet every year, and distance driven

      return np.array(electric_emissions)/10**12,np.array(tailpipe_emissions)/10**12,np.array(ev_prod_emissions)/10**9,\
                  np.array(ice_prod_emissions)/10**9,np.array(conv_prod_emissions)/10**9,np.array(mod_shift_emiss),\
                  np.array(cum_electric),cum_tailpipe,cum_ev_prod,cum_ice_prod,cum_conv_prod,cum_mod_shift_emiss,\
                  np.array(elec_demand),foss_demand,ev_prod_energy,ice_prod_energy,conv_prod_energy,mod_shift_energy,\
                  cum_elec,cum_foss,cum_ev_en,cum_ice_en,cum_conv_en,cum_mod_en,ages,km_driven

#Run base case
base=Run_Model(phase_out_date=2030,phase_out_hybrid=2035,scrap_age_pre2020=20,scrap_age_post2020=15,mass=1400,fleet_size_projection=20,miles_driven_projection=20,retrofit_percentage=0,manufacture=0,elec=2050,rate=28)