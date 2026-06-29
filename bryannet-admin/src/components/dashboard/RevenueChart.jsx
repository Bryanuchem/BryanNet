import { useState } from "react";

import {
    Skeleton,
    Typography,
} from "@mui/material";

import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

import DashboardSection from "../common/DashboardSection";
import CardHeader from "../common/CardHeader";

import useRevenueOverview from "../../hooks/useRevenueOverview";

const FILTER_OPTIONS = [
    {
        value: "7d",
        label: "Last 7 Days",
    },
    {
        value: "30d",
        label: "Last 30 Days",
    },
    {
        value: "month",
        label: "This Month",
    },
    {
        value: "12m",
        label: "Last 12 Months",
    },
];

const currencyFormatter = (value) =>
    `₦${Number(value).toLocaleString()}`;

function RevenueChart() {

    const [period, setPeriod] = useState("month");

    const {
        data = [],
        isLoading,
    } = useRevenueOverview(period);

    return (

        <DashboardSection

            header={

                <CardHeader
                    title="Revenue Overview"
                    value={period}
                    onChange={(event) =>
                        setPeriod(event.target.value)
                    }
                    options={FILTER_OPTIONS}
                />

            }

        >

            {isLoading ? (

                <Skeleton
                    variant="rounded"
                    height={320}
                />

            ) : data.length === 0 ? (

                <Typography
                    align="center"
                    color="text.secondary"
                    sx={{
                        py: 14,
                    }}
                >
                    No revenue data available.
                </Typography>

            ) : (

                <ResponsiveContainer
                    width="100%"
                    height={320}
                >

                    <LineChart
                        data={data}
                        margin={{
                            top: 15,
                            right: 20,
                            left: 10,
                            bottom: 10,
                        }}
                    >

                        <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                        />

                        <XAxis
                            dataKey="label"
                            tickLine={false}
                            axisLine={false}
                        />

                        <YAxis
                            width={80}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={currencyFormatter}
                        />

                        <Tooltip
                            formatter={(value) => [
                                currencyFormatter(value),
                                "Revenue",
                            ]}
                        />

                        <Line
                            type="monotone"
                            dataKey="revenue"
                            stroke="#1976d2"
                            strokeWidth={3}
                            dot={{ r: 4 }}
                            activeDot={{ r: 7 }}
                        />

                    </LineChart>

                </ResponsiveContainer>

            )}

        </DashboardSection>

    );

}

export default RevenueChart;