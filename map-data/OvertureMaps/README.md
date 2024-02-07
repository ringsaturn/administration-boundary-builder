# Global Admin Boundary GeoJSON from Overture Maps

> **NOTE**
>
> Please make sure read Overture Maps'
> [dataset License](https://github.com/OvertureMaps/schema/blob/v0.5.0/README.md)
> before using it.

Other references:

- <https://github.com/OvertureMaps/schema>
- <https://github.com/overtureMaps/data>

## Download

```bash
mkdir -p themes/admins
cd themes/admins
# Download admin data, about 600MB
aws s3 cp --recursive --region us-west-2 --no-sign-request s3://overturemaps-us-west-2/release/2023-07-26-alpha.0/theme=admins/ .
```

## Build all in one GeoJSON file

You can find installation guide here: <https://duckdb.org/#quickinstall>

```bash
duckdb
```

Install `spatial` extension:

```sql
INSTALL spatial;
```

Load extension:

```sql
LOAD spatial;
```

Build GeoJSON file:

```sql
--- Revised from: https://github.com/OvertureMaps/data/blob/main/duckdb_queries/admins.sql
COPY (
    SELECT
        type,
        id,
        subType,
        localityType,
        adminLevel,
        isoCountryCodeAlpha2,
        JSON(bbox) AS bbox,
        JSON(names) AS names,
        JSON(sources) AS sources,
        ST_GeomFromWkb(geometry) AS geometry
    FROM
        read_parquet(
            './type=*/*',
            filename = true,
            hive_partitioning = 1
        )
    WHERE
        ST_GeometryType(ST_GeomFromWkb(geometry)) IN ('POLYGON', 'MULTIPOLYGON')
) TO 'countries.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON');
```
