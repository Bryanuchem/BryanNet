import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createPayment,
} from "../api/payments";

export default function useCreatePayment() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: createPayment,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["payments"],
            });

        },

    });

}