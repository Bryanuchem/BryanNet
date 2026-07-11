// ==========================================================
// Payment Providers
// ==========================================================

export const PaymentProvider = {

    MANUAL: "manual",

};


// ==========================================================
// Payment Channels
// ==========================================================

export const PaymentChannel = {

    CASH: "cash",

    BANK_TRANSFER: "bank_transfer",

    CARD: "card",

    USSD: "ussd",

    WALLET: "wallet",

    SYSTEM: "system",

};


// ==========================================================
// Payment Status
// ==========================================================

export const PaymentStatus = {

    PENDING: "pending",

    SUCCESSFUL: "successful",

    FAILED: "failed",

    CANCELLED: "cancelled",

    REFUNDED: "refunded",

    EXPIRED: "expired",

};


// ==========================================================
// Payment Provider Options
// ==========================================================

export const PAYMENT_PROVIDER_OPTIONS = [

    {

        value: PaymentProvider.MANUAL,

        label: "Manual",

    },

];


// ==========================================================
// Payment Channel Options
// ==========================================================

export const PAYMENT_CHANNEL_OPTIONS = [

    {

        value: PaymentChannel.CASH,

        label: "Cash",

    },

    {

        value: PaymentChannel.BANK_TRANSFER,

        label: "Bank Transfer",

    },

    {

        value: PaymentChannel.CARD,

        label: "Card",

    },

    {

        value: PaymentChannel.USSD,

        label: "USSD",

    },

    {

        value: PaymentChannel.WALLET,

        label: "Wallet",

    },

    {

        value: PaymentChannel.SYSTEM,

        label: "System",

    },

];


// ==========================================================
// Payment Status Options
// ==========================================================

export const PAYMENT_STATUS_OPTIONS = [

    {

        value: PaymentStatus.PENDING,

        label: "Pending",

    },

    {

        value: PaymentStatus.SUCCESSFUL,

        label: "Successful",

    },

    {

        value: PaymentStatus.FAILED,

        label: "Failed",

    },

    {

        value: PaymentStatus.CANCELLED,

        label: "Cancelled",

    },

    {

        value: PaymentStatus.REFUNDED,

        label: "Refunded",

    },

    {

        value: PaymentStatus.EXPIRED,

        label: "Expired",

    },

];