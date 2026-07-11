type Props = {
  rows: Record<string, unknown>[];
};

const KPICards = ({ rows }: Props) => {

  if (rows.length === 0) {

    return null;

  }

  const columns = Object.keys(rows[0]);

  const numericColumns = columns.filter(column =>

    rows.every(row =>

      typeof row[column] === "number"

    )

  );

  const firstNumericColumn = numericColumns[0];

  let average: number | null = null;

  let minimum: number | null = null;

  let maximum: number | null = null;

  if (firstNumericColumn) {

    const values = rows.map(

      row => Number(row[firstNumericColumn])

    );

    average =
      values.reduce((a, b) => a + b, 0) / values.length;

    minimum = Math.min(...values);

    maximum = Math.max(...values);

  }

  const formatValue = (
  value: number | null
) => {

  if (value === null) {

    return "-";

  }

  return value.toLocaleString(

    "fr-FR",

    {

      minimumFractionDigits: 0,

      maximumFractionDigits: 2,

    }

  );

};

  return (

    <div
      className="
        grid
        grid-cols-1 
        md:grid-cols-2 
        xl:grid-cols-4
        gap-4
        mb-6
      "
    >

      <Card

        title="📊 Résultats"

        value={rows.length}

      />

      {

        firstNumericColumn && (

          <>

            <Card

              title={`💰 Moyenne (${firstNumericColumn})`}

              value={formatValue(average)}

            />

            <Card

              title={`📈 Maximum (${firstNumericColumn})`}

              value={formatValue(maximum)}

            />

            <Card

              title={`📉 Minimum (${firstNumericColumn})`}

              value={formatValue(minimum)}

            />

          </>

        )

      }

    </div>

  );

};

type CardProps = {

  title: string;

  value: string | number | undefined | null;

};

function Card({

  title,

  value,

}: CardProps) {

  return (

    <div
      className="
        rounded-xl
        border
        border-gray-700
        bg-[#202020]
        p-5
      "
    >

      <div className="text-sm text-gray-400">

        {title}

      </div>

      <div className="mt-2 text-3xl font-bold">

        {value}

      </div>

    </div>

  );

}

export default KPICards;