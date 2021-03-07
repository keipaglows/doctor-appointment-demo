<template>
  <section class="section section-components">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <base-button class="btn-3" type="primary" icon="ni ni-bold-left" outline
                       @click="goToTheFirstStep()">
            Go to the first step
          </base-button>

          <tabs fill class="flex-column flex-md-row" ref="tabs">
            <card shadow slot-scope="{activeTabIndex}">
              <div class="mb-3">
                <span class="font-weight-bold text-primary display-5">
                  {{stepInfo[activeTabIndex]}}
                </span>
              </div>
              <tab-pane key="tab1">
                <template slot="title">
                  <i class="ni ni-badge mr-2"></i>Doctors
                </template>

                <doctor-list @doctorSet="doctorSet"></doctor-list>
              </tab-pane>

              <tab-pane key="tab2">
                <template slot="title">
                  <i class="ni ni-building mr-2"></i>Offices
                </template>

                <office-list ref="office_list" @officeSet="officeSet"></office-list>
              </tab-pane>

              <tab-pane key="tab3">
                <template slot="title">
                  <i class="ni ni-calendar-grid-58 mr-2"></i>Contact Info
                </template>

                <appointment-panel @appointmentCreated="appointmentCreated"></appointment-panel>
              </tab-pane>
            </card>
          </tabs>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Tabs from "@/components/Tabs/Tabs.vue"
import TabPane from "@/components/Tabs/TabPane.vue"

import DoctorList from "./DoctorList.vue"
import OfficeList from "./OfficeList.vue"
import AppointmentPanel from "./AppointmentPanel.vue"

export default {
  components: {
    AppointmentPanel,
    DoctorList,
    OfficeList,
    Tabs,
    TabPane
  },
  data() {
    return {
      stepInfo: {
        0: 'Select a doctor',
        1: 'Select an office',
        2: 'Fill your contact info, then select date and time'
      }
    }
  },
  methods: {
    goToTheFirstStep() {
      this.$refs.tabs.activateTab(this.$refs.tabs.tabs[0]);
    },
    doctorSet() {
      // loading offices and displaying respective tab
      this.$refs.office_list.loadOffices()
      this.$refs.tabs.activateTab(this.$refs.tabs.tabs[1]);
    },
    officeSet() {
      // setting active the final tab with contact info
      this.$refs.tabs.activateTab(this.$refs.tabs.tabs[2]);
    },
    appointmentCreated() {
      this.$refs.tabs.activateTab(this.$refs.tabs.tabs[0]);
    }
  }
};
</script>

<style>
</style>
