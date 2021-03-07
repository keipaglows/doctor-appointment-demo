<template>
  <div>
    <div class="row justify-content-md-center">
      <div class="col-lg-6">
        <small class="d-block text-uppercase font-weight-bold mb-3">First Name</small>
        <base-input v-model="patient.first_name">
        </base-input>

        <small class="d-block text-uppercase font-weight-bold mb-3">Last Name</small>
        <base-input v-model="patient.last_name">
        </base-input>

        <small class="d-block text-uppercase font-weight-bold mb-3">Gender</small>
        <div class="form-group">
          <select class="form-control" v-model="patient.gender">
            <option v-for="gender in genders"
                    v-bind:key="gender.value"
                    v-bind:value="gender.value">
              {{gender.text}}
            </option>
          </select>
        </div>

        <small class="d-block text-uppercase font-weight-bold mb-3">Email</small>
        <base-input v-model="patient.email">
        </base-input>
      </div>

      <div class="col-lg-6">
        <small class="d-block text-uppercase font-weight-bold mb-3">Schedule Date</small>
        <base-input addon-left-icon="ni ni-calendar-grid-58">
          <flat-picker class="form-control datepicker"
                       slot-scope="{focus, blur}"
                       @on-open="focus"
                       @on-close="blur"
                       :config="datePickerConfig"
                       v-model="scheduledDateTime">
          </flat-picker>
        </base-input>

        <small class="d-block text-uppercase font-weight-bold mb-3">Selected Doctor</small>
        <base-input :value="selectedDoctor" :disabled=true>
        </base-input>

        <small class="d-block text-uppercase font-weight-bold mb-3">Selected Office</small>
        <base-input :value="selectedOffice" :disabled=true>
        </base-input>
      </div>
        
      <base-button class="mb-3 mb-sm-0" type="success" outline @click="makeAppointment()">
        Make an appointment
      </base-button>
    </div>

    <modal :show.sync="showSuccessModal"
            gradient="success"
            modal-classes="modal-danger modal-dialog-centered">
      <div class="py-3 text-center">
        <i class="ni ni-bell-55 ni-3x"></i>
        <h4 class="heading mt-4">Success</h4>
        
        <div class="text-left">
          <div class="display-4 py-3">Appoinment has been made!</div>

          <div class="row py-1 align-items-center">
            <div class="col-sm-3">
              <small class="text-uppercase white font-weight-bold">Doctor:</small>
            </div>
            
            <div class="col-sm-9">{{selectedDoctor}}</div>
          </div>

          <div class="row py-1 align-items-center">
            <div class="col-sm-3">
              <small class="text-uppercase white font-weight-bold">Office:</small>
            </div>
            
            <div class="col-sm-9">{{selectedOffice}}</div>
          </div>

          <div class="row py-1 align-items-center">
            <div class="col-sm-3">
              <small class="text-uppercase white font-weight-bold">Scheduled:</small>
            </div>
            
            <div class="col-sm-9">{{scheduledDateTime}}</div>
          </div>
        </div>
      </div>

      <template slot="footer">
        <base-button type="white"
                     @click="closeSuccessModal()">
          Ok, Got it
        </base-button>
      </template>
    </modal>

    <modal :show.sync="showFailModal"
            gradient="danger"
            modal-classes="modal-danger modal-dialog-centered">
      <div class="py-3 text-center">
        <i class="ni ni-bell-55 ni-3x"></i>
        <h4 class="heading mt-4">Errors</h4>
        
        <div class="text-left" v-for="error in formErrors" :key="error.key">
          {{error.key}}: {{error.value}}
        </div>
      </div>

      <template slot="footer">
        <base-button type="white"
                      @click="showFailModal = false">
          Ok, Got it
        </base-button>
      </template>
    </modal>
  </div>
</template>

<script>
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";

import Modal from "@/components/Modal.vue";

export default {
  components: {
    flatPicker,
    Modal
  },
computed: {
  selectedDoctor() {
    const doctor = this.$store.state.doctor

    if (doctor) {
      return `${doctor.last_name} ${doctor.first_name}`
    }
  },
  selectedOffice() {
    const office = this.$store.state.office

    if (office) {
      return office.name
    }
  }
},
  data() {
    return {
      formErrors: [],
      showSuccessModal: false,
      showFailModal: false,
      datePickerConfig: {
        allowInput: true,
        enableTime: true,
        time_24hr: true,
        minDate: 'today'
      },
      genders: [
        {text: 'Male', value: 'Male'},
        {text: 'Female', value: 'Female'},
        {text: 'Other', value: 'Other'}
      ],
      patient: {
        first_name: null,
        last_name: null,
        email: null,
        gender: 'Male'
      },
      scheduledDateTime: null
    }
  },
  methods: {
    makeAppointment() {
      const post_data = {
        'doctor_id': this.$store.state.doctor.id,
        'office_id': this.$store.state.office.id,
        'scheduled_datetime': this.$data.scheduledDateTime,
        'patient': this.$data.patient
      }

      this.axios.post('http://localhost:8010/api/appointments', post_data).then(
        response => this.handleSuccess(response)
      ).catch(
        response => this.handleErrors(response)
      )
    },
    closeSuccessModal() {
      this.$data.showSuccessModal = false
      this.$emit('appointmentCreated')
      this.resetData()
    },
    resetData() {
      this.$data.patient.first_name = null
      this.$data.patient.last_name = null
      this.$data.patient.email = null
      this.$data.patient.gender = 'Male'
      this.$data.scheduledDateTime = null

      this.$store.commit('setDoctor', null)
      this.$store.commit('setOffice', null)
    },
    handleSuccess(response) {
      console.log(response)
      this.$data.showSuccessModal = true
    },
    handleErrors(response) {
      this.$data.formErrors = []
      this.formatErrors(response.response.data.errors)
      this.$data.showFailModal = true
    },
    formatErrors(error, errorKey) {
      const isObject = typeof error === 'object'
      const isArray = Array.isArray(error)

      if (isObject && !isArray) {
        for (const [key, value] of Object.entries(error)) {
          this.formatErrors(value, key)
        }
      } else {
        if (isArray) {
          error = error[0]
        }
        
        this.$data.formErrors.push({
          'key': errorKey,
          'value': error
        })
      }
    }
  }
}
</script>

<style>
</style>
