 const nameInput = document.getElementById('getmedicine');
            const quantityInput = document.getElementById('getquantity');
            const MFGInput = document.getElementById('getMFG');
            const expiryInput = document.getElementById('getexpiry');
            const AmountInput = document.getElementById('getSell_Amount');
            const output = document.getElementById('output');
            const outputexp = document.getElementById('outputep');
        
            // Handle input field for live search
            nameInput.addEventListener('input', function () {
                const search = nameInput.value.toLowerCase().trim(); // Trim whitespace
                let found = false;
        
                medicines.forEach(med => {
                    if (med.name.toLowerCase().includes(search)) {
                        console.log(`Expiry: ${med.expiry}`);
                        console.log(`Search : ${med.name}`);
                        output.innerHTML = med.name;
                        outputexp.innerHTML = med.expiry ;// Update the output div with matched name
                        found = true;
                    }
                });
        
                if (!found) {
                    output.innerHTML = "No match found."; // Display message for no match
                }
            });
        
            // Populate input fields when a match is selected
            function AddData() {
                const addsearch = output.innerHTML.trim().toLowerCase(); // Trim and convert to lowercase
        
                let found = false;
                medicines.forEach(add => {
                    if (add.name.toLowerCase() === addsearch) { // Exact match for the medicine name
                        nameInput.value = add.name;
                        quantityInput.value = add.quantity;
                        MFGInput.value = add.MFG;
                        expiryInput.value = add.expiry;
                        AmountInput.value = add.rate;
                        found = true;
                    }
                });
        
                if (!found) {
                    alert("Error: No matching medicine found.");
                }
            }




            const PostMedicines = [];

function AddMedicine() {
    let post_id; // Changed to let for later assignment
    let post_name;
    let post_rate; // Changed to let for later assignment
    const post_sell_quantity = document.getElementById('getSell_quantity').value; // Access value directly
    const convert_amount = document.getElementById('getSell_Amount').value; // Access value directly
    const post_amount = post_sell_quantity * convert_amount; // Calculate total amount
    let total_amuont_bill = 0; 
    // Get search input for medicine matching
    const search = document.getElementById('getmedicine').value.toLowerCase();

    let found = false;

    medicines.forEach(med => {
        if (med.name.toLowerCase().includes(search)) { // Case-insensitive match
            console.log(`Search Match: ${med.name}`);
            post_id = med.id; // Assign the matched medicine ID
            post_name = med.name;
            post_rate = med.rate // Assign the matched medicine name
            found = true;

            PostMedicines.push({
                data_id: post_id, // Corrected syntax for object property
                data_name: post_name, // Corrected syntax for object property
                data_amount: post_amount,
                data_rete : post_rate,
                data_sell_quantity: post_sell_quantity, // Corrected syntax for object property
                
                // Corrected syntax for object property
            });
        }

    });

    PostMedicines.forEach((med ,index )=> {
        if (index === PostMedicines.length - 1) { // Check if it's the last element
        
        // Perform actions with the last item
        
        // Case-insensitive match
                    const table = document.getElementById("MedicineTable").getElementsByTagName("tbody")[0];
                    const newRow = table.insertRow();
            
                    newRow.innerHTML = `
                        <td class="theditno" ><input type="text" class="inputdatatd" value="${med.data_id}" name="medicine_id" readonly></td>
                        <td><input type="text" readonly class="inputdata" value="${index + 1}" name="count" ></td>
                        <td><input type="text" readonly class="inputdata" value="${med.data_name}" name="medicine"></td>
                        <td><input type="text" readonly class="inputdata" value="${med.data_sell_quantity}" name="Sell_quantity"></td>
                        <td><input type="text" readonly class="inputdata" value="${med.data_amount}" name="Sell_amount"></td>
                        
                    `;
}});

PostMedicines.forEach(med => {
    total_amuont_bill += parseFloat(med.data_amount) || 0; // Add the current amount to the total
     // Log the updated total after each iteration
});
  document.getElementById('total_amount_display').value =total_amuont_bill;
console.log(total_amuont_bill);


function deleteRow(button) {
    const row = button.parentElement.parentElement; // Locate the row
    row.remove();
}

function submitfrom(){

    fetch('sell_medicin_all_process', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json', // Specify JSON payload
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Include CSRF token
    },
    body: JSON.stringify(PostMedicines) // Convert JavaScript object to JSON string
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch(error => {
    console.error('Error:', error);
});
}
    // Log the PostMedicines array
   
}


