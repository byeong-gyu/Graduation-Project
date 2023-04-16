package gradu.gradu.repository;

import gradu.gradu.domain.Board;
import gradu.gradu.domain.BoardFile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BoardFileRepository extends JpaRepository<BoardFile, Long> {
    BoardFile findByBoard(Board board);
}
