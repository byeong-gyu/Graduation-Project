package gradu.gradu.domain;

import lombok.*;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Getter
@Builder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
public class BoardFile {

    @Id
    @GeneratedValue
    private Long id;

    private String originalFileName;

    private String storedFileName;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="board_id")
    private Board board;

    private LocalDateTime boardTime;

    public void setBoard(Board board){
        this.board=board;
        board.getBoardFileList().add(this);
    }
}
