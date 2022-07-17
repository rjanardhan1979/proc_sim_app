<template>
<h1>{{x}}</h1>
</template>

<script>


export default {
  name: 'App',
  components: {    
  },
  data() {
    return {
      x: []
    }
  },
  async created() {
  //const response = await fetch('http://localhost:8000');  
  const filter = await fetch('http://localhost:8000/proc_type/primary%20hip')
  const result = await filter.json()
  this.x = result
  },
}
</script>

<style>

</style>
