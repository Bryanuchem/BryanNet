export function formatPhoneNumber(phoneNumber) {
    if (!phoneNumber) {
        return "-";
    }

    if (
        phoneNumber.startsWith("234") &&
        phoneNumber.length === 13
    ) {
        return `+${phoneNumber.slice(0, 3)} ${phoneNumber.slice(3, 6)} ${phoneNumber.slice(6, 9)} ${phoneNumber.slice(9)}`;
    }

    return phoneNumber;
}

export function formatStatus(status) {
    if (!status) {
        return "-";
    }

    return status.charAt(0).toUpperCase() + status.slice(1);
}