'use client';

import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import UsersTable from "@/components/ui/UsersTable";
import { useState } from "react";
import AreaChartCard from "@/components/ui/charts/AreaChart";
import BarChartCard from "@/components/ui/charts/BarChart";

export default function DashboardHome() {
  const [search, setSearch] = useState("");

  return (
    <div className="p-6 space-y-6">

      {/* Page Header*/}
      <h1 className="text-4xl font-bold">Dashboard</h1>

      <p className="text-lg italic font-light bg-gray-300 p-2">
        Welcome to the administrative dashboard. This section provides a consolidated view of system activity,
        user engagement, and operational performance. The data presented here is designed to support informed
        decision-making through clear visual indicators and summarized metrics.
      </p>

      {/* Stats Fixed Cards*/}
      <section id="stats" className="scroll-mt-20">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card title="Primary Card" variant="primary" content="primary">
            <Button variant="primary">View Details <span className="pl-10">&#8250;</span></Button>
          </Card>
          <Card title="Warning Card" variant="warning" content="warning">
            <Button variant="warning">View Details <span className="pl-10">&#8250;</span></Button>
          </Card>
          <Card title="Success Card" variant="success" content="success">
            <Button variant="success">View Details <span className="pl-10">&#8250;</span></Button>
          </Card>
          <Card title="Danger Card" variant="danger" content="danger">
            <Button variant="danger">View Details <span className="pl-10">&#8250;</span></Button>
          </Card>
        </div>
      </section>

      {/* Chart Cards*/}
      <section id="charts" className="scroll-mt-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 mt-6">
          <AreaChartCard />
          <BarChartCard />
        </div>
      </section>

      {/* Table Card*/}
      <section id="users" className="scroll-mt-20">
        <Card title="&#128203;  DataTable Example" variant="table" content="table">
          <div className="flex flex-col mx-auto w-full">
            <UsersTable search={search} />
          </div>
        </Card >
      </section>

    </div >
  );
}
