import {
    useMutation,
} from "@tanstack/react-query";

import {
    getPaymentReceipt,
} from "../api/payments";


export function usePaymentReceipt() {

    return useMutation({

        mutationFn: async (
            paymentReference,
        ) => {

            const blob =
                await getPaymentReceipt(
                    paymentReference,
                );

            const url =
                window.URL.createObjectURL(
                    blob,
                );

            window.open(
                url,
                "_blank",
            );

            setTimeout(() => {

                window.URL.revokeObjectURL(
                    url,
                );

            }, 1000);

        },

    });

}