<template>
  <div class="flex flex-col h-full">
    <div class="overflow-y-auto">
      <table
        class="w-full text-center p-5 text-sm border-collapse text-gray-500"
      >
        <thead
          class="display-table table-fixed sticky top-0 text-xs text-white uppercase bg-gray-400"
        >
          <tr>
            <th
              v-for="key in myDataKeys"
              :key="key.id"
              scope="col"
              class="py-3 px-6"
            >
              {{ key }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in myData"
            :key="index"
            class="bg-white border-b hover:bg-gray-100"
          >
            <td v-for="key in myDataKeys" :key="key.id" class="py-4 px-6">
              {{ this.myData[index][key] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "myTable",
  props: {
    myData: Object,
    myDataKeys: Object,
  },
};
</script>
