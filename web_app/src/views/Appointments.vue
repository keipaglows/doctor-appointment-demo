<template>
  <section class="section section-components pb-0" id="section-components">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <h2 class="mb-5">
            <span>Doctor Appointments Demo</span>
          </h2>

          <appointment-tabs></appointment-tabs>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import AppointmentTabs from './components/AppointmentTabs.vue';

export default {
  name: "appointments",
  components: {
    AppointmentTabs
  }
};
</script>

<style>
</style>
