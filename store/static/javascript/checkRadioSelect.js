const radioButtons = document.querySelectorAll(".btn-check");
const checked = false

const validateForm = () => {
    radioButtons.forEach((btn) => {
        if (btn.checked) {
            checked = true;
        }
    })
    if (!checked) {
        alert("Please select a size.")
        return false;
    }
    return true;
}