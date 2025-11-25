import React, { useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  ColumnDef,
  SortingState,
  ColumnFiltersState,
} from '@tanstack/react-table';
import { Finding } from '../../services/api';

interface FindingsTableProps {
  data: Finding[];
  onRowClick?: (finding: Finding) => void;
}

const FindingsTable: React.FC<FindingsTableProps> = ({ data, onRowClick }) => {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const columns = useMemo<ColumnDef<Finding>[]>(
    () => [
      {
        accessorKey: 'title',
        header: 'Title',
        cell: (info) => info.getValue(),
      },
      {
        accessorKey: 'focus_area',
        header: 'Focus Area',
        cell: (info) => {
          const focusArea = info.row.original.focus_area;
          return focusArea?.name || 'N/A';
        },
      },
      {
        accessorKey: 'issue_type',
        header: 'Issue Type',
        cell: (info) => {
          const issueType = info.row.original.issue_type;
          return issueType?.name || 'N/A';
        },
      },
      {
        accessorKey: 'severity',
        header: 'Severity',
        cell: (info) => {
          const severity = info.getValue() as string;
          const colors: Record<string, string> = {
            Critical: 'bg-danger',
            High: 'bg-warning',
            Medium: 'bg-info',
            Low: 'bg-success',
          };
          return (
            <span className={`badge ${colors[severity] || 'bg-secondary'}`}>
              {severity}
            </span>
          );
        },
      },
      {
        accessorKey: 'risk_assessment',
        header: 'Risk Score',
        cell: (info) => {
          const score = info.row.original.risk_assessment?.risk_score || 0;
          return <span>{score}</span>;
        },
      },
      {
        accessorKey: 'money_loss_calculation',
        header: 'Money Loss',
        cell: (info) => {
          const loss = info.row.original.money_loss_calculation?.estimated_loss || 0;
          return <span>${loss.toLocaleString()}</span>;
        },
      },
      {
        accessorKey: 'detected_at',
        header: 'Detected',
        cell: (info) => {
          const date = new Date(info.getValue() as string);
          return date.toLocaleDateString();
        },
      },
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <div>
      <div className="mb-3">
        <input
          type="text"
          value={globalFilter ?? ''}
          onChange={(e) => setGlobalFilter(e.target.value)}
          placeholder="Search findings..."
          className="form-control"
        />
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    style={{ cursor: header.column.getCanSort() ? 'pointer' : 'default' }}
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                    {{
                      asc: ' ↑',
                      desc: ' ↓',
                    }[header.column.getIsSorted() as string] ?? null}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                onClick={() => onRowClick && onRowClick(row.original)}
                style={{ cursor: onRowClick ? 'pointer' : 'default' }}
              >
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FindingsTable;

