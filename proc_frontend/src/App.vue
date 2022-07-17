<template>
  <div class="grid grid-cols-4 grid-rows-6 gap-4 p-5 h-screen">
    <div
      class="navbar shadow-lg bg-white p-4 rounded-lg col-span-1 row-span-full"
    >
      <div class="grid grid-cols-3 justify-start">
        <img src="./assets/images/freelogo.png" class="col-span-1" alt="" />
        <h1 class="class= col-span-2 flex justify-center items-center text-2xl">
          Jamadu
        </h1>
      </div>

      <div
        class="grid grid-rows-3 grid-cols-1 w-full gap-6 justify-start py-10"
      >
        <div
          class="form-select row-span-1 px-3 py-1.5 text-sm font-medium text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-300 focus:bg-white focus:outline-none"
          aria-label="Default select example"
        >
          <select
            class="w-full"
            name=""
            v-model="procedure"
            id=""
            @change="refresh()"
          >
            <option value="primary knee">primary knee</option>
            <option value="primary hip">primary hip</option>
          </select>
        </div>
        <div
          class="form-select row-span-2 appearance-none block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
          aria-label="Default select example"
        >
          <label
            for="entitlement"
            class="mb-2 text-sm font-medium text-gray-700 flex justify-center items-center"
            >Select Entitlement</label
          >
          <input
            id="entitlement"
            v-model="entitlement_val"
            type="range"
            min="1"
            max="15"
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
          />
          <label
            class="mt-2 text-sm font-medium text-gray-700 flex justify-center items-center"
            >{{ entitlement_val }}</label
          >
        </div>
      </div>
    </div>
    <div
      class="section shadow-lg bg-white p-10 rounded-lg col-span-3 row-span-5"
    >
      <test-table :myData="myData" :myDataKeys="myDataKeys" />
    </div>
    <div
      class="footer shadow-lg bg-green-100 text-green-500 text-lg font-bold text-center p-10 rounded-lg row-start-6 col-start-2 col-span-3 row-span-1"
    >
      2
    </div>
  </div>
</template>

<script>
import testTable from "./components/testTable.vue";
export default {
  name: "App",
  components: { testTable },
  data() {
    return {
      myData: null,
      myDataKeys: null,
      entitlement_val: 8,
      procedure: "primary knee",
    };
  },
  async created() {
    this.refresh();
  },
  methods: {
    async refresh() {
      const filter = await fetch(
        "http://localhost:8000/proc_type/" + this.procedure
      );
      const result = await filter.json();
      this.myData = result;
      this.myDataKeys = Object.keys(this.myData[0]);
    },
  },
};
</script>

<style></style>
