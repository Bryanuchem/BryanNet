import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    deletePayment,
} from "../api/payments";

export default function useDeletePayment() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: deletePayment,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["payments"],
            });

        },

    });

}