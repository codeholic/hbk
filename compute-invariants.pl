use strict;
use warnings;

use autodie;

use IO::Handle ();
use List::MoreUtils 'uniq';
use Math::Combinatorics 'combine';

my @invariants = get_invariants(g_getcells(g_getselrect()));
g_exit("@invariants");

sub get_invariants {
    my ($cells) = @_;

    my @invariants;
    foreach my $t (0 .. 3) {
        my @gliders;
        my $temp_cells = [ @$cells ];
        foreach my $gen (0 .. 3) {
            push @gliders, map { [ @$_, $gen ] } find_all_gliders($temp_cells);
            $temp_cells = g_evolve($temp_cells, 1);
        }

        my @glider_pairs = combine(2, @gliders);
        foreach my $pair (@glider_pairs) {
            push @invariants, compute_invariants(@$pair);
        }

        $cells = g_transform($cells, 0, 0, 0, -1, 1, 0);
    }

    return uniq(@invariants);
}

sub find_all_gliders {
    my ($cells) = @_;

    my $map = {};
    for (my $c = 0; $c < @$cells; $c += 2) {
        my ($x, $y) = @$cells[$c, $c + 1];
        $map->{$x}{$y}++;
    }

    my @ret;
    POSITION: for (my $c = 0; $c < @$cells; $c += 2) {
        my ($x, $y) = @$cells[$c, $c + 1];

        my $glider_map = {
            $x     => { $y     => 1, $y + 2 => 1 },
            $x + 1 => { $y + 1 => 1, $y + 2 => 1 },
            $x + 2 => { $y + 1 => 1 },
        };

        for (my $i = $x - 1; $i < $x + 4; $i++) {
            for (my $j = $y - 1; $j < $y + 4; $j++) {
                next POSITION if $map->{ $i }{ $j } xor $glider_map->{ $i }{ $j };
            }
        }

        push @ret, [$x, $y];
    }

    return @ret;
}

sub compute_invariants {
    my ($g1, $g2) = @_;

    my $dx = $g2->[0] - $g1->[0];
    my $dy = $g2->[1] - $g1->[1];
    my $dt = $g2->[2] - $g1->[2];

    my $hd = $dx - $dy;
    my $tr = $hd / 2 * 47;

    return abs($dt - 4 * $dy - $tr), abs(4 * $dx - $dt - $tr);
}
