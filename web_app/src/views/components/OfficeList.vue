<template>
  <table class="table table-hover">
    <thead class="thead-light">
      <tr>
        <th>Name</th>
        <th>Start Time</th>
        <th>End Time</th>
        <th>Phone Number</th>
      </tr>
    </thead>

    <tbody class="list">
      <tr v-for="office in offices"
          :key="office.id"
          @click="setOffice(office)">
        <td>{{office.name}}</td>
        <td>{{office.start_time}}</td>
        <td>{{office.end_time}}</td>
        <td>{{office.phone_number}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  data() {
    return {
      offices: null
    }
  },
  methods: {
    loadOffices() {
      const doctorId = this.$store.state.doctor.id

      this.axios.get(`http://localhost:8010/api/offices?doctor_id=${doctorId}`).then(
        response => {
          this.$data.offices = response.data.results
        }
      )
    },
    setOffice(office) {
      this.$store.commit('setOffice', office)
      this.$emit('officeSet')
    }
  }
}
</script>

<style>
</style>
