<template>


    <table class="text-center p-5 text-sm  border-collapse text-gray-500 dark:text-gray-400">
        <thead class="display-table table-fixed sticky top-0 text-xs text-gray-700 
        uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th v-for="key in myDataKeys" :key="key.id" scope="col" class="py-3 px-6">
                    {{key}}
                </th>
            </tr>
        </thead>
        <tbody class=" divide-y">
            <tr v-for="(row, index) in myData" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50
              dark:hover:bg-gray-600">

                <td v-for="key in myDataKeys" :key="key.id" class="py-4 px-6">
                    {{this.myData[index][key]}}
                </td>
                
            </tr>            
        </tbody>
    </table>

    
</template>

<script>
export default {
    name: 'myTable',
    props: {
        myData: Object,
        myDataKeys: Object,
    }
}
</script>