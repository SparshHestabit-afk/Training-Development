'use client';

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Card from "../Card";
import { chartData } from "./chartsData";

export default function AreaChartCard() {
    return (
        <Card title="&#128200;  Area Chart Example" variant="area" content="area">
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Area
                            type="monotone"
                            dataKey="users"
                            stroke="#2563eb"
                            fill="#93c5fd"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </Card>
    );
}