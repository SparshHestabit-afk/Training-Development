'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Card from "../Card";
import { chartData } from "./chartsData";

export default function BarChartCard() {
    return (
        <Card title="&#128202;  Bar Chart Example" variant="bar" content="bar">
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="2 2" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="sales" fill="#16a34a" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </Card>
    );
}