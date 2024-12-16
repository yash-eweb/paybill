document.addEventListener('DOMContentLoaded', function () {
    const warrantyStatusSelect = document.getElementById('warranty_status');
    const rememberExpiryDateCheckbox = document.getElementById('remember_expiry_date');
    const expiryDateContainer = document.getElementById('expiry_date_container');
    const rememberExpiryDateContainer = document.getElementById('remember_expiry_date_container');
    const expiryDateInput = document.getElementById('expiry_date');
    const form = document.getElementById('billForm');

    // Function to toggle fields based on warranty status
    function toggleFields() {
        const warrantyStatus = warrantyStatusSelect.value;
        const rememberExpiryDateChecked = rememberExpiryDateCheckbox.checked;

        if (warrantyStatus === "under_warranty") {
            expiryDateContainer.style.display = "block";
            expiryDateInput.required = true; // Expiry date is required
            rememberExpiryDateContainer.style.display = "none"; // Hide "I don’t remember expiry date" checkbox
            rememberExpiryDateCheckbox.checked = false; // Uncheck checkbox
        } else if (warrantyStatus === "expired") {
            expiryDateContainer.style.display = "block"; // Show expiry date field by default
            rememberExpiryDateContainer.style.display = "block"; // Show "I don’t remember expiry date" checkbox

            // If "I don’t remember expiry date" is checked, hide expiry date field
            if (rememberExpiryDateChecked) {
                expiryDateContainer.style.display = "none";
                expiryDateInput.required = false; // Expiry date is not required
                expiryDateInput.value = ""; // Clear expiry date value
            }
            else {
                expiryDateInput.required = true; // Expiry date is required
            }

             
            
        } else {
            expiryDateContainer.style.display = "none";
            expiryDateInput.required = false; // Expiry date is not required
            rememberExpiryDateContainer.style.display = "none";
        }
    }

    expiryDateInput.addEventListener("input", function () {
        if (expiryDateInput.value) {
            rememberExpiryDateContainer.style.display = "none"; // Hide checkbox when a date is entered
            rememberExpiryDateCheckbox.checked = false; // Uncheck the checkbox
        } else {
            rememberExpiryDateContainer.style.display = "block"; // Show checkbox if date is cleared
        }
    });


    // Function to validate form on submit
    function validateForm(event) {
        const warrantyStatus = warrantyStatusSelect.value;
        const expiryDate = expiryDateInput.value;
        const rememberExpiryDateChecked = rememberExpiryDateCheckbox.checked;

        // Validation: "under_warranty" requires an expiry date
        if (warrantyStatus === "under_warranty" && !expiryDate) {
            alert("Expiry date is required for bills under warranty.");
            event.preventDefault();
        }

        // Validation: "expired" with "I don’t remember expiry date" unchecked requires an expiry date
        if (warrantyStatus === "expired" && !rememberExpiryDateChecked && !expiryDate) {
            alert("Please provide an expiry date or select 'I don’t remember the expiry date.'");
            event.preventDefault();
        }

        // Validation: "expired" with "I don’t remember expiry date" checked must not have an expiry date
        if (warrantyStatus === "expired" && rememberExpiryDateChecked && expiryDate) {
            alert("Expiry date should not be provided if you don’t remember it.");
            event.preventDefault();
        }
    }

    // Attach event listeners
    warrantyStatusSelect.addEventListener("change", toggleFields);
    rememberExpiryDateCheckbox.addEventListener("change", toggleFields);
    form.addEventListener("submit", validateForm);

    // Initialize fields on page load
    toggleFields();
});
