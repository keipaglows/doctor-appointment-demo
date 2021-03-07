<template>
  <table class="table table-hover">
    <thead class="thead-light">
      <tr>
        <th>Name</th>
        <th>Specialty</th>
        <th>Job Title</th>
        <th>Email</th>
        <th>Office Phone</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="doctor in doctors"
          :key="doctor.id"
          @click="setDoctor(doctor)">
        <td>{{doctor.last_name}} {{doctor.first_name}}</td>
        <td>{{doctor.specialty}}</td>
        <td>{{doctor.job_title}}</td>
        <td>{{doctor.email}}</td>
        <td>{{doctor.office_phone}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  mounted() {
    this.loadDoctors()
  },
  data() {
    return {
      doctors: null
    }
  },
  methods: {
    loadDoctors() {
      this.axios.get('http://localhost:8010/api/doctors').then(
        response => {
          this.$data.doctors = response.data.results
        }
      )
    },
    setDoctor(doctor) {
      this.$store.commit('setDoctor', doctor)
      this.$emit('doctorSet')
    }
  }
}
</script>

<style>
</style>
